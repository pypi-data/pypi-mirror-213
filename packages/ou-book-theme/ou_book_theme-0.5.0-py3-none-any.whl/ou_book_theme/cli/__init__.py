"""OU Book Theme CLI application."""
import typer

from datetime import datetime
from importlib.resources import files, as_file
from lxml import etree
from os import path, makedirs
from rich import print as stdout
from rich.progress import Progress
from shutil import rmtree, copy
from subprocess import run
from yaml import safe_load

from ..__about__ import __version__


app = typer.Typer()


def xpath_single(start: etree.Element, xpath: str):
    """Retrieve a single element using XPath."""
    return start.xpath(xpath)[0]


def create_text_node(tag: str, text: str) -> etree.Element:
    """Create a new text node."""
    element = etree.Element(tag)
    element.text = text
    return element


def fix_sub_list(node: etree.Element):
    """Fix the nested list tags."""
    # Fix sub lists so that they use the correct tags
    if node.tag == 'BulletedList':
        node.tag = 'BulletedSubsidiaryList'
    elif node.tag == 'NumberedList':
        node.tag = 'NumberedSubsidiaryList'
    elif node.tag == 'ListItem':
        node.tag = 'SubListItem'
    for child in node:
        fix_sub_list(child)


def apply_fixes(
        config: dict,
        source: str,
        node: etree.Element,
        module_code: str,
        block: int,
        part: int,
        presentation: str,
        counters: dict,
        part_title: str
    ) -> None:
    """Apply a range of post-processing fixes."""
    # Postprocessing required:
    # * Remove non-document cross-links
    if node.tag == 'ComputerDisplayBlock':
        # Add paragraphs into block-level computer displays
        node.tag = 'ComputerDisplay'
        lines = node.text.split('\n')
        if lines[-1].strip() == '':
            lines = lines[:-1]
        node.text = None
        for line in lines:
            para = etree.Element('Paragraph')
            para.text = line
            node.append(para)
    elif node.tag == 'Reference':
        # Remove paragraphs from references
        if len(node) == 1:
            node.text = node[0].text
            para = node[0]
            del node[0]
            node.extend(para)
    elif node.tag == 'Table':
        # Fix table heads
        thead = None
        tbody = None
        has_caption = False
        for child in node:
            if child.tag == 'thead':
                thead = child
            elif child.tag == 'tbody':
                tbody = child
            elif child.tag == 'TableHead':
                has_caption = True
        if thead is not None and tbody is not None:
            for row in thead:
                for cell in row:
                    cell.tag = 'th'
                    cell.attrib['class'] = 'ColumnHeadLeft'
            for row in reversed(thead):
                tbody.insert(0, row)
            node.remove(thead)
        if not has_caption:
            node.insert(0, create_text_node('TableHead', ''))
    elif node.tag == 'Title':
        # Add numbers to the titles
        if node.getparent().tag == 'Introduction':
            if 'overwrite' in config['ou'] and 'introduction_title' in config['ou']['overwrite']:
                node.text = config['ou']['overwrite']['introduction_title']
        if node.getparent().tag in ['Introduction', 'Session']:
            counters['session'] = counters['session'] + 1
            node.text = f'{counters["session"]} {node.text}'
            counters['section'] = 0
        elif node.getparent().tag == 'Section':
            counters['section'] = counters['section'] + 1
            node.text = f'{counters["session"]}.{counters["section"]} {node.text}'
    elif node.tag == 'Caption':
        # Add figure numbering
        if node.getparent().tag == 'Figure':
            counters['figure'] = counters['figure'] + 1
            node.text = f'Figure {counters["figure"]} {node.text}'
    elif node.tag == 'TableHead':
        # Add table numbering
        counters['table'] = counters['table'] + 1
        node.text = f'Table {counters["table"]} {node.text}'
    elif node.tag == 'Mermaid':
        # Render the Mermaid graphs
        mermaid_cli = files('ou_book_theme.cli') / 'mermaid-cli'
        with as_file(mermaid_cli) as mermaid_cli_path:
            run(['npm', 'install'], cwd=mermaid_cli_path, capture_output=True)
            filename = f'{module_code.lower()}_b{block}_p{part}_{presentation.lower()}_fig{counters["figure"]}.png'
            filepath = path.join(source, '_build', 'ouxml', filename)
            run([
                    path.join(mermaid_cli_path, 'node_modules', '.bin', 'mmdc'),
                    '-i',
                    '-',
                    '-o',
                    filepath
                ],
                input=node.text.encode(),
                capture_output=True)
            img = etree.Element('Image')
            img.attrib['src'] = filename
            node.getparent().replace(node, img)
    elif node.tag == 'Image':
        # Copy images
        image_src = path.join(source, node.attrib['src'])
        if path.exists(image_src):
            filename = f'{module_code.lower()}_b{block}_p{part}_{presentation.lower()}_fig{counters["figure"]}.png'
            filepath = path.join(source, '_build', 'ouxml', filename)
            copy(image_src, filepath)
            node.attrib['src'] = filename
    elif node.tag == 'Activity':
        # Wrap the activity content in a Question
        question = None
        for child in list(node):
            if child.tag not in ['Heading', 'Timing', 'Question', 'Answer']:
                if question is None:
                    question = etree.Element('Question')
                    node.replace(child, question)
                    question.append(child)
                else:
                    question.append(child)
    elif node.tag == 'meta':
        # Fix the meta attribute part title
        node.attrib['content'] = node.attrib['content'].replace('$PART_TITLE', part_title)
    elif node.tag == 'BulletedList':
        for list_item in node:
            for child in list_item:
                fix_sub_list(child)
    if node.text is not None and '$PART_TITLE' in node.text:
        # Fix any in-text part titles
        node.text = node.text.replace('$PART_TITLE', part_title)
    for child in node:
        apply_fixes(config, source, child, module_code, block, part, presentation, counters, part_title)


def transform_content(
        node: etree.Element,
        root_node: str='Section'
    ) -> etree.Element:
    """Apply the XSLT transforms from Sphinx XML to OU XML."""
    stylesheet = etree.XML(f'''\
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <!-- Section templates -->
    <xsl:template match="/section">
        <{root_node}><xsl:apply-templates/></{root_node}>
    </xsl:template>
    <xsl:template match="section">
        <InternalSection><xsl:apply-templates/></InternalSection>
    </xsl:template>

    <!-- Heading templates -->
    <xsl:template match="/section/title">
        <Title><xsl:apply-templates/></Title>
    </xsl:template>
    <xsl:template match="title">
        <Heading><xsl:apply-templates/></Heading>
    </xsl:template>

    <!-- Paragraph templates -->
    <xsl:template match="paragraph">
        <Paragraph><xsl:apply-templates/></Paragraph>
    </xsl:template>

    <!-- Admonition templates -->
    <xsl:template match="admonition">
        <Box><xsl:apply-templates/></Box>
    </xsl:template>
    <xsl:template match="hint">
        <Box><Heading>Hint</Heading><xsl:apply-templates/></Box>
    </xsl:template>
    <xsl:template match="warning">
        <Box><Heading>Warning</Heading><xsl:apply-templates/></Box>
    </xsl:template>
    <xsl:template match="attention">
        <Box><Heading>Attention</Heading><xsl:apply-templates/></Box>
    </xsl:template>
    <xsl:template match="note">
        <Box><Heading>Note</Heading><xsl:apply-templates/></Box>
    </xsl:template>

    <!-- Code block templates -->
    <xsl:template match="inline[@classes = 'guilabel']">
        <ComputerUI><xsl:apply-templates/></ComputerUI>
    </xsl:template>
    <xsl:template match="inline[@classes = 'menuselection']">
        <ComputerUI><xsl:apply-templates/></ComputerUI>
    </xsl:template>
    <xsl:template match="literal_block">
        <ComputerDisplayBlock><xsl:apply-templates/></ComputerDisplayBlock>
    </xsl:template>
    <xsl:template match="literal">
        <ComputerCode><xsl:apply-templates/></ComputerCode>
    </xsl:template>

    <!-- List templates -->
    <xsl:template match="bullet_list">
        <BulletedList><xsl:apply-templates/></BulletedList>
    </xsl:template>
    <xsl:template match="enumerated_list">
        <NumberedList><xsl:apply-templates/></NumberedList>
    </xsl:template>
    <xsl:template match="list_item">
        <ListItem><xsl:apply-templates/></ListItem>
    </xsl:template>

    <!-- Styling templates -->
    <xsl:template match="emphasis"><i><xsl:apply-templates/></i></xsl:template>
    <xsl:template match="strong"><b><xsl:apply-templates/></b></xsl:template>

    <!-- Reference templates -->
    <xsl:template match="number_reference">
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="number_reference/inline">
        <xsl:value-of select="text()"/>
    </xsl:template>
    <xsl:template match="reference[@internal = 'True' and @refuri]" priority="10">
        <olink>
            <xsl:attribute name="targetdoc">
                <xsl:value-of select="@refuri"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </olink>
    </xsl:template>
    <xsl:template match="reference[@refuri]">
        <a>
            <xsl:attribute name="href">
                <xsl:value-of select="@refuri"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </a>
    </xsl:template>
    <xsl:template match="reference/inline">
        <xsl:value-of select="text()"/>
    </xsl:template>
    <xsl:template match="citation">
        <Reference><xsl:apply-templates/></Reference>
    </xsl:template>
    <xsl:template match="citation/label"></xsl:template>

    <!-- Figure templates -->
    <xsl:template match="figure">
        <Figure><xsl:apply-templates/></Figure>
    </xsl:template>
    <xsl:template match="image">
        <Image>
            <xsl:attribute name="src">
                <xsl:value-of select="@uri"/>
            </xsl:attribute>
        </Image>
    </xsl:template>
    <xsl:template match="caption">
        <Caption><xsl:apply-templates/></Caption>
    </xsl:template>

    <!-- Activity templates -->
    <xsl:template match="container[@design_component = 'ou-activity']">
        <Activity><xsl:apply-templates/></Activity>
    </xsl:template>
    <xsl:template match="container[@design_component = 'ou-activity-title']">
        <Heading><xsl:apply-templates/></Heading>
    </xsl:template>
    <xsl:template match="container[@design_component = 'ou-time']">
        <Timing><xsl:apply-templates/></Timing>
    </xsl:template>
    <xsl:template match="container[@design_component = 'ou-activity-answer']">
        <Answer><xsl:apply-templates/></Answer>
    </xsl:template>

    <!-- Where next templates -->
    <xsl:template match="container[@design_component = 'ou-where-next']">
        <Box><Heading>Now go to ...</Heading><xsl:apply-templates/></Box>
    </xsl:template>

    <!-- TOC Tree templates -->
    <xsl:template match="compound[@classes = 'toctree-wrapper']"></xsl:template>

    <!-- Mermaid templates -->
    <xsl:template match="mermaid">
        <Mermaid><xsl:value-of select="@code"/></Mermaid>
    </xsl:template>

    <!-- Quote templates -->
    <xsl:template match="block_quote">
        <Quote><xsl:apply-templates/></Quote>
    </xsl:template>

    <!-- Cross-reference templates -->
    <xsl:template match="inline[@ids]"><xsl:apply-templates/></xsl:template>
    <xsl:template match="container[@ids]"><xsl:apply-templates/></xsl:template>

    <!-- Table templates -->
    <xsl:template match="table">
        <Table><xsl:apply-templates/></Table>
    </xsl:template>
    <xsl:template match="table/title">
        <TableHead><xsl:apply-templates/></TableHead>
    </xsl:template>
    <xsl:template match="tgroup"><xsl:apply-templates/></xsl:template>
    <xsl:template match="colspec"><xsl:apply-templates/></xsl:template>
    <xsl:template match="tbody">
        <tbody><xsl:apply-templates/></tbody>
    </xsl:template>
    <xsl:template match="thead">
        <thead><xsl:apply-templates/></thead>
    </xsl:template>
    <xsl:template match="row">
        <tr><xsl:apply-templates/></tr>
    </xsl:template>
    <xsl:template match="entry">
        <td><xsl:apply-templates/></td>
    </xsl:template>

    <xsl:template match="*">
        <UnknownTag><xsl:value-of select="name(.)"/></UnknownTag>
    </xsl:template>
</xsl:stylesheet>''')
    transform = etree.XSLT(stylesheet)
    return transform(xpath_single(node, '/document/section')).getroot()


def create_introduction(input_base: str, root: etree.Element, chapter: dict) -> None:
    """Create the introduction structure."""
    with open(path.join(input_base, f'{chapter["file"]}.xml')) as in_f:
        doc = etree.parse(in_f)
        introduction = transform_content(
            doc,
            root_node='Introduction'
        )
        if 'sections' in chapter:
            for section in chapter['sections']:
                create_section(input_base, introduction, section)
        root.append(introduction)


def create_section(input_base: str, root: etree.Element, section: dict) -> None:
    """Create the structure for a single section, which writes to a single part file."""
    with open(path.join(input_base, f'{section["file"]}.xml')) as in_f:
        doc = etree.parse(in_f)
        section = transform_content(
            doc,
            root_node='Section'
        )
        root.append(section)


def create_session(input_base: str, root: etree.Element, chapter: dict) -> None:
    """Create a sesssion within a file."""
    with open(path.join(input_base, f'{chapter["file"]}.xml')) as in_f:
        doc = etree.parse(in_f)
        session = transform_content(
            doc,
            root_node='Session'
        )
        if 'sections' in chapter:
            for section in chapter['sections']:
                create_section(input_base, session, section)
        root.append(session)


def create_unit(config: dict, root: etree.Element, part: dict, input_base: str, unit_id: str, unit_title: str) -> None:
    """Create a single unit."""
    unit = etree.Element('Unit')
    root.append(unit)
    unit.append(create_text_node('UnitID', unit_id))
    unit.append(create_text_node('UnitTitle', unit_title))
    unit.append(create_text_node('ByLine', config['author']))
    for chapter_idx, chapter in enumerate(part['chapters']):
        if chapter_idx == 0:
            create_introduction(input_base, unit, chapter)
        else:
            create_session(input_base, unit, chapter)


def create_frontmatter(root: etree.Element, config: dict) -> None:
    """Create the frontmatter XML structure."""
    frontmatter = etree.XML(f'''\
<FrontMatter>
  <ByLine>{config["author"]}</ByLine>
  <Imprint>
    <Standard>
      <GeneralInfo>
        <Paragraph>This publication forms part of the Open University module {config["ou"]["module_code"]} {config["ou"]["module_title"]}. [The complete list of texts which make up this module can be found at the back (where applicable)]. Details of this and other Open University modules can be obtained from the Student Registration and Enquiry Service, The Open University, PO Box 197, Milton Keynes MK7 6BJ, United Kingdom (tel. +44 (0)845 300 60 90; email general-enquiries@open.ac.uk).</Paragraph>
        <Paragraph>Alternatively, you may visit the Open University website at www.open.ac.uk where you can learn more about the wide range of modules and packs offered at all levels by The Open University.</Paragraph>
        <Paragraph>To purchase a selection of Open University materials visit www.ouw.co.uk, or contact Open University Worldwide, Walton Hall, Milton Keynes MK7 6AA, United Kingdom for a brochure (tel. +44 (0)1908 858793; fax +44 (0)1908 858787; email ouw-customer-services@open.ac.uk).</Paragraph>
      </GeneralInfo>
      <Address>
        <AddressLine>The Open University,</AddressLine>
        <AddressLine>Walton Hall, Milton Keynes</AddressLine>
        <AddressLine>MK7 6AA</AddressLine>
      </Address>
      <FirstPublished>
        <Paragraph>First published {config["ou"]["first_published"]}</Paragraph>
      </FirstPublished>
      <Copyright>
        <Paragraph>Copyright © {datetime.now().year} The Open University</Paragraph>
      </Copyright>
      <Rights>
        <Paragraph>All rights reserved. No part of this publication may be reproduced, stored in a retrieval system, transmitted or utilised in any form or by any means, electronic, mechanical, photocopying, recording or otherwise, without written permission from the publisher or a licence from the Copyright Licensing Agency Ltd. Details of such licences (for reprographic reproduction) may be obtained from the Copyright Licensing Agency Ltd, Saffron House, 6–10 Kirby Street, London EC1N 8TS (website www.cla.co.uk).</Paragraph>
        <Paragraph>Open University materials may also be made available in electronic formats for use by students of the University. All rights, including copyright and related rights and database rights, in electronic materials and their contents are owned by or licensed to The Open University, or otherwise used by The Open University as permitted by applicable law.</Paragraph>
        <Paragraph>In using electronic materials and their contents you agree that your use will be solely for the purposes of following an Open University course of study or otherwise as licensed by The Open University or its assigns.</Paragraph>
        <Paragraph>Except as permitted above you undertake not to copy, store in any medium (including electronic storage or use in a website), distribute, transmit or retransmit, broadcast, modify or show in public such electronic materials in whole or in part without the prior written consent of The Open University or in accordance with the Copyright, Designs and Patents Act 1988.</Paragraph>
      </Rights>
      <Edited>
        <Paragraph>Edited and designed by The Open University.</Paragraph>
      </Edited>
      <Typeset>
        <Paragraph>Typeset by The Open University</Paragraph>
      </Typeset>
      <Printed>
        <Paragraph>Printed and bound in the United Kingdom by [name and address of the printer].</Paragraph>
        <Paragraph />
      </Printed>
      <ISBN>{config["ou"]["isbn"]}</ISBN>
      <Edition>{config["ou"]["edition"]}</Edition>
    </Standard>
  </Imprint>
</FrontMatter>
''')
    root.append(frontmatter)


def create_root(config: dict, file_id: str, title: str) -> etree.Element:
    """Create the root structure."""
    module_code = config['ou']['module_code']
    module_title = config['ou']['module_title']

    root = etree.Element('Item')
    root.attrib['TextType'] = 'CompleteItem'
    root.attrib['SchemaVersion'] = '2.0'
    root.attrib['id'] = file_id
    root.attrib['Template'] = 'Generic_A4_Unnumbered'
    root.attrib['Rendering'] = 'VLE2 staff (learn3)'
    root.attrib['DiscussionAlias'] = 'Comment'
    root.attrib['Autonumber'] = 'false'
    root.attrib['vleglossary'] = 'manual'
    meta = etree.Element('meta')
    meta.attrib['content'] = title
    root.append(meta)
    root.append(create_text_node('CourseCode', module_code))
    root.append(create_text_node('CourseTitle', module_title))
    root.append(etree.Element('ItemID'))
    root.append(create_text_node('ItemTitle', title))

    return root


@app.command()
def convert_to_ouxml(source: str, regenerate: bool=False, numbering_from: int=1):
    """Convert the content into OU XML."""
    input_base = path.join(source, '_build', 'xml')
    if not path.exists(input_base) or regenerate:
        result = run(['jb', 'build', '--builder', 'custom', '--custom-builder', 'xml', source])
        stdout('')
        if result.returncode == 0:
            stdout('[green]XML (re)built[/green] ✓')
            stdout('')
            stdout('[bold]Converting to OU XML[/bold]')
        else:
            stdout('[red]XML building failed[/red]')
            return
    if not path.exists(input_base):
        stdout(f'[red]Source XML directory {input_base} does not exist. Please build this first.[/red]')
    with Progress() as progress:
        clearing_task = progress.add_task('Preparing', total=3)
        output_base = path.join(source, '_build', 'ouxml')
        if path.exists(output_base):
            rmtree(output_base)
        makedirs(output_base, exist_ok=True)
        progress.update(clearing_task, completed=1)

        with open(path.join(source, '_toc.yml')) as in_f:
            toc = safe_load(in_f)
        progress.update(clearing_task, completed=2)
        with open(path.join(source, '_config.yml')) as in_f:
            config = safe_load(in_f)
        progress.update(clearing_task, completed=3)

        if 'parts' in toc:
            main_task = progress.add_task('Converting', total=len(toc['parts']))
            module_code = config['ou']['module_code']
            block = int(config['ou']['block'])
            presentation = config['ou']['presentation']
            for part_idx, part in enumerate(toc['parts']):
                part_idx = numbering_from + part_idx
                root = create_root(
                    config,
                    f'X_{module_code.lower()}_b{block}_p{part_idx}_{presentation.lower()}',
                    f'{module_code} Block {block}, Part {part_idx}: $PART_TITLE'
                )
                create_frontmatter(root, config)
                create_unit(
                    config,
                    root,
                    part,
                    input_base,
                    f'Block {block}: {config["ou"]["block_title"]}',
                    f'{part["caption"]}: $PART_TITLE',
                )
                part_title = xpath_single(root, '/Item/Unit/Introduction/Title/text()')
                apply_fixes(config, source, root, module_code, block, part_idx, presentation, {'session': 0, 'section': 0, 'figure': 0, 'table': 0}, part_title)
                with open(path.join(output_base, f'{module_code.lower()}_b{block}_p{part_idx}_{presentation.lower()}.xml'), 'wb') as out_f:
                    out_f.write(etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True))
                progress.update(main_task, advance=1)
        else:
            main_task = progress.add_task('Converting', total=1)
            module_code = config['ou']['module_code']
            block = config['ou']['block']
            presentation = config['ou']['presentation']
            root = create_root(
                config,
                f'X_{module_code.lower()}_{block.lower()}_{presentation.lower()}',
                f'{module_code} {block}: $PART_TITLE'
            )
            create_frontmatter(root, config)
            create_unit(
                config,
                root,
                toc,
                input_base,
                f'{block}: $PART_TITLE',
                f'{module_code} {block}: $PART_TITLE'
            )
            part_title = xpath_single(root, '/Item/Unit/Introduction/Title/text()')
            apply_fixes(config, source, root, module_code, block, 0, presentation, {'session': 0, 'section': 0, 'figure': 0, 'table': 0}, part_title)
            with open(path.join(output_base, f'{module_code.lower()}_{block.lower()}.xml'), 'wb') as out_f:
                out_f.write(etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True))
            progress.update(main_task, advance=1)


@app.command()
def version():
    """Print the current version."""
    stdout(__version__)


def main():
    """Run the OBT application."""
    app()
