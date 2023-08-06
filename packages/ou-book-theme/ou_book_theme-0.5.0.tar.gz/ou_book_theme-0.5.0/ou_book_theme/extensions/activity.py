"""Additional Sphinx directives for OU activities."""
from docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx_design.shared import is_component, create_component


class ActivityDirective(SphinxDirective):
    """The ActivityDirective directive is used to generate an activity block."""

    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        activity = create_component(
            'ou-activity',
            rawtext=self.content
        )
        activity += create_component(
            'ou-activity-title',
            rawtext=self.arguments[0],
            children=[nodes.Text(self.arguments[0], self.arguments[0])]
        )
        self.state.nested_parse(self.content, self.content_offset, activity)
        return [activity]


class ActivityHtmlTransform(SphinxPostTransform):
    """Transform activity containers into the HTML specific AST structures."""

    default_priority = 198
    formats = ("html",)

    def run(self):
        """Run the transform"""
        document: nodes.document = self.document
        for node in document.findall(lambda node: is_component(node, "ou-activity")):
            newnode = create_component(
                'ou-activity',
                classes=['ou-activity'],
            )
            title_node = create_component(
                'ou-activity-title',
                classes=['ou-activity-title'],
                children=node.children[0].children
            )
            newnode += title_node
            newnode += node.children[1:]
            node.replace_self(newnode)


class ActivityAnswerDirective(SphinxDirective):
    """The ActivityAnswerDirective directive is used to generate an activity block."""

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        activity_answer = create_component(
            'ou-activity-answer',
            classes=['ou-activity-answer'],
            rawtext=self.content,
        )
        self.state.nested_parse(self.content, self.content_offset, activity_answer)
        return [activity_answer]


class ActivityAnswerHtmlTransform(SphinxPostTransform):
    """Transform activity containers into the HTML specific AST structures."""

    default_priority = 199
    formats = ("html",)

    def run(self):
        """Run the transform"""
        document: nodes.document = self.document
        for node in document.findall(lambda node: is_component(node, "ou-activity-answer")):
            newnode = create_component(
                'ou-activity-answer',
                classes=['ou-activity-answer'],
            )
            newnode += nodes.raw('', '<hr/>', format='html')
            newnode += nodes.raw(
                '',
                '<button class="sd-btn sd-btn-info ou-toggle ou-toggle-hidden"><span class="ou-toggle-show">Show answer</span><span class="ou-toggle-hide">Hide answer</span></button>',
                format='html',
            )
            content_container = create_component(
                'ou-activity-answer-content',
                classes=['ou-activity-answer-content'],
                children = node.children
            )
            newnode += content_container
            node.replace_self(newnode)


def setup(app):
    """Setup the Activity extensions."""
    app.add_directive('activity', ActivityDirective)
    app.add_directive('activity-answer', ActivityAnswerDirective)
    app.add_post_transform(ActivityHtmlTransform)
    app.add_post_transform(ActivityAnswerHtmlTransform)
