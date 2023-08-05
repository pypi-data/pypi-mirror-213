from __future__ import annotations

import re
from contextlib import suppress
from typing import Any, Iterable, Union


def conform_attribute_name(key: str) -> str:
    """
    Format an attribute name to fit the standard.
    """
    key = key.strip('_')
    key = re.sub(r'[^a-zA-Z0-9_-]+', "", key)
    key = key.replace('_', '-')
    return key

    
def prepare_attributes(*attrs: str, **kwattrs: Any) -> tuple[set[str], dict[str, Any]]:
    """
    Prepare positional and keyword attributes.
    Fit to standards and remove duplicates.
    """

    # Format attribute names to fit standard.
    attrs = set([conform_attribute_name(attr) for attr in attrs])
    kwattrs = {conform_attribute_name(attr): value for attr, value in kwattrs.items()}

    # Remove duplicates based on the type of the keyword argument
    for attr, value in list(kwattrs.items()):
        if value in (False, None):
            kwattrs.pop(attr)
        elif value is True:
            kwattrs.pop(attr)
            attrs.add(attr)
        elif attr in attrs:
            attrs.pop(attr)

    return attrs, kwattrs


def render_html_element(tag: str, content: str, /, *attrs: str, **kwattrs: Any) -> str:
    """
    Render HTML element from tag, content,
    positional arguments, and keyword arguments.


    If content is left as None, the element will remain unclosed.
    E.g. <p> as opposed to <p></p>


    Python:
        render_html_element('dialog', 'Hello, World!', 'open', class_='greeting')
    HTML:
        "<dialog open class='greeting'>Hello, World!</dialog>"
    """

    attrs, kwattrs = prepare_attributes(*attrs, **kwattrs)

    elm = f'<{tag}'

    # Append all positional arguments
    for attr in attrs:
        elm += f' {attr}'

    # Append all keyword arguments
    for attr, value in kwattrs.items():
        elm += f' {attr}={str(value)!r}'

    # Close tag off if content is provided
    if content is not None:
        return f'{elm}>{content}</{tag}>'
    else:
        return f'{elm}>'


Content = Union[str, 'HTMLTag', Iterable]


class HTMLTag:
    """
    Base class for all HTML tags

    Inherit from it to define a new tag type.
    Ex. `class landscape(HTMLTag): ...`
    """

    tag: str
    attrs: set[str]
    kwattrs: dict[str, str]
    children: list[Any]


    def __init__(self, *attrs: str, **kwattrs: Any) -> None:
        self.attrs, self.kwattrs = prepare_attributes(*attrs, **kwattrs)
        self.children = None

    def __init_subclass__(cls) -> None:
        # Define a new tag by inheriting from HTMLTag.
        # The tag name will be the name of the class.
        cls.tag = cls.__name__

        # Strip appended underscore from tag
        if cls.tag.endswith('_'):
            cls.tag = cls.tag[:-1]

    def __str__(self) -> str:
        return self.render(pretty=False)

    def __gt__(self, content: Content, /) -> HTMLTag:
        """
        Return a copy with the children added.
        """

        # Create a copy of the element
        copy = type(self)(*self.attrs, **self.kwattrs)
        
        if self.children is not None:
            copy.add(self.children)

        # Add children

        # o) Strings and HTML tags are obviously singular
        if isinstance(content, (str, HTMLTag)):
            return copy.add(content)
        
        # o) Any iterable should be unravelled
        # and have its elements added
        if isinstance(content, Iterable):
            return copy.add(*content)
        
        # o) Anything else, add it singularly
        return copy.add(content)

    def __contains__(self, attribute: str, /) -> bool:
        """
        Get whether tag has attribute.
        """
        return attribute in self.attrs \
            or attribute in self.kwattrs

    def __delitem__(self, attribute: str, /) -> None:
        """
        Remove attribute.
        """
        with suppress(KeyError):
            self.attrs.remove(attribute)
        with suppress(KeyError):
            self.kwattrs.pop(attribute)

    __isub__ = __delitem__

    def __iadd__(self, attribute: str, /) -> None:
        """
        Add positional attribute.
        """
        if attribute not in self.kwattrs:
            self.attrs.add(attribute)
        return self

    def __getitem__(self, attribute: str, /) -> Any:
        """
        Get attribute.
        """
        if attribute in self.kwattrs:
            return self.kwattrs[attribute]
        if attribute in self.attrs:
            return True
        return False

    def __setitem__(self, attribute: str, value: Any, /) -> None:
        """
        Set attribute.
        """

        with suppress(KeyError):
            if value in (False, None):
                del self[attribute]
            elif value is True:
                self.attrs.add(attribute)
                self.kwattrs.pop(attribute)
            else:
                self.kwattrs[attribute] = value
                self.attrs.remove(attribute)


    def render(self, pretty: bool = False) -> str:
        """
        Render HTML element from tag, content,
        positional arguments, and keyword arguments.
        """

        # o) Unclosed tag
        if self.children is None:
            return render_html_element(self.tag, None, *self.attrs, **self.kwattrs)

        # o) Closed and pretty
        if pretty:
            content = ""
            for child in self.children:
                if isinstance(child, HTMLTag):
                    child = child.render(pretty=pretty)

                for line in str(child).splitlines():
                    content += f"\n    {line}"

            if content != "":
                content = f'{content}\n'

            return render_html_element(self.tag, content, *self.attrs, **self.kwattrs)

        # o) Closed and inline
        children = []
        for child in self.children:
            if isinstance(child, HTMLTag):
                children.append(child.render(pretty=False))
            else:
                children.append(child)

        content = "".join(map(str, children))
        return render_html_element(self.tag, content, *self.attrs, **self.kwattrs)

    def add(self, *elements: HTMLTag | str) -> HTMLTag:
        """
        Add children.
        """
        if self.children is None:
            self.children = []
        self.children.extend(elements)
        return self



# AN EXTENSIVE LIST OF HTML ELEMENTS
# 
# Descriptions used were found at W3Schools.com
# https://www.w3schools.com/tags/default.asp


class a(HTMLTag):
    """
    Defines a hyperlink
    """

class abbr(HTMLTag):
    """
    Defines an abbreviation or an acronym
    """

class acronym(HTMLTag):
    """
    Defines an acronym

    Not supported in HTML5.
    Use <abbr> instead.
    """

class address(HTMLTag):
    """
    Defines contact information for the author/owner of a document
    """

class applet(HTMLTag):
    """
    Defines an embedded applet

    Not supported in HTML5.
    Use <embed> or <object> instead.
    """

class area(HTMLTag):
    """
    Defines an area inside an image map
    """

class article(HTMLTag):
    """
    Defines an article
    """

class aside(HTMLTag):
    """
    Defines content aside from the page content
    """

class audio(HTMLTag):
    """
    Defines embedded sound content
    """

class b(HTMLTag):
    """
    Defines bold text
    """

class base(HTMLTag):
    """
    Specifies the base URL/target for all relative URLs in a document
    """

class basefont(HTMLTag):
    """
    Specifies a default color, size, and font for all text in a document

    Not supported in HTML5. Use CSS instead.
    """

class bdo(HTMLTag):
    """
    Overrides the current text direction
    """

class big(HTMLTag):
    """
    Defines big text

    Not supported in HTML5. Use CSS instead.
    """

class blockquote(HTMLTag):
    """
    Defines a section that is quoted from another source
    """

class body(HTMLTag):
    """
    Defines the document's body
    """

class br(HTMLTag):
    """
    Defines a single line break
    """

class button(HTMLTag):
    """
    Defines a clickable button
    """

class canvas(HTMLTag):
    """
    Used to draw graphics, on the fly, via scripting (usually JavaScript)
    """

class caption(HTMLTag):
    """
    Defines a table caption
    """

class center(HTMLTag):
    """
    Defines centered text

    Not supported in HTML5. Use CSS instead.
    """

class cite(HTMLTag):
    """
    Defines the title of a work
    """

class code(HTMLTag):
    """
    Defines a piece of computer code
    """

class col(HTMLTag):
    """
    Specifies column properties for each column within a <colgroup> element
    """

class colgroup(HTMLTag):
    """
    Specifies a group of one or more columns in a table for formatting
    """

class datalist(HTMLTag):
    """
    Specifies a list of pre-defined options for input controls
    """

class dd(HTMLTag):
    """
    Defines a description/value of a term in a description list
    """

class del_(HTMLTag):
    """
    Defines text that has been deleted from a document
    """

class details(HTMLTag):
    """
    Defines additional details that the user can view or hide
    """

class dfn(HTMLTag):
    """
    Specifies a term that is going to be defined within the content
    """

class dialog(HTMLTag):
    """
    Defines a dialog box or window
    """

class dir_(HTMLTag):
    """
    Defines a directory list

    Not supported in HTML5.
    Use <ul> instead.
    """

class div(HTMLTag):
    """
    Defines a section in a document
    """

class dl(HTMLTag):
    """
    Defines a description list
    """

class dt(HTMLTag):
    """
    Defines a term/name in a description list
    """

class em(HTMLTag):
    """
    Defines emphasized text
    """

class embed(HTMLTag):
    """
    Defines a container for an external application
    """

class fieldset(HTMLTag):
    """
    Groups related elements in a form
    """

class figcaption(HTMLTag):
    """
    Defines a caption for a <figure> element
    """

class figure(HTMLTag):
    """
    Specifies self-contained content
    """

class font(HTMLTag):
    """
    Defines font, color, and size for text

    Not supported in HTML5. Use CSS instead.
    """

class footer(HTMLTag):
    """
    Defines a footer for a document or section
    """

class form(HTMLTag):
    """
    Defines an HTML form for user input
    """

class frame(HTMLTag):
    """
    Defines a window (a frame) in a frameset

    Not supported in HTML5.
    """

class frameset(HTMLTag):
    """
    Defines a set of frames

    Not supported in HTML5.
    """

class h1(HTMLTag):
    """
     Defines a level 1 heading
    """

class h2(HTMLTag):
    """
     Defines a level 2 heading
    """

class h3(HTMLTag):
    """
     Defines a level 3 heading
    """

class h4(HTMLTag):
    """
     Defines a level 4 heading
    """

class h5(HTMLTag):
    """
     Defines a level 5 heading
    """

class h6(HTMLTag):
    """
     Defines a level 6 heading
    """

class head(HTMLTag):
    """
    Contains metadata/information for the document
    """

class header(HTMLTag):
    """
    Defines a header for a document or section
    """

class hr(HTMLTag):
    """
     Defines a thematic change in the content
    """

class html(HTMLTag):
    """
    Defines the root of an HTML document
    """

class i(HTMLTag):
    """
    Defines a part of text in an alternate voice or mood
    """

class iframe(HTMLTag):
    """
    Defines an inline frame
    """

class img(HTMLTag):
    """
    Defines an image
    """

class input_(HTMLTag):
    """
    Defines an input control
    """

class ins(HTMLTag):
    """
    Defines a text that has been inserted into a document
    """

class kbd(HTMLTag):
    """
    Defines keyboard input
    """

class label(HTMLTag):
    """
    Defines a label for an <input> element
    """

class legend(HTMLTag):
    """
    Defines a caption for a <fieldset> element
    """

class li(HTMLTag):
    """
    Defines a list item
    """

class main(HTMLTag):
    """
    Specifies the main content of a document
    """

class map_(HTMLTag):
    """
    Defines an image map
    """

class mark(HTMLTag):
    """
    Defines marked/highlighted text
    """

class meta(HTMLTag):
    """
    Defines metadata about an HTML document
    """

class meter(HTMLTag):
    """
    Defines a scalar measurement within a known range (a gauge)
    """

class nav(HTMLTag):
    """
    Defines navigation links
    """

class noframes(HTMLTag):
    """
    Defines an alternate content for users that do not support frames

    Not supported in HTML5.
    """

class object_(HTMLTag):
    """
    Defines a container for an external application
    """

class ol(HTMLTag):
    """
    Defines an ordered list
    """

class optgroup(HTMLTag):
    """
    Defines a group of related options in a drop-down list
    """

class option(HTMLTag):
    """
    Defines an option in a drop-down list
    """

class output(HTMLTag):
    """
    Defines the result of a calculation
    """

class p(HTMLTag):
    """
    Defines a paragraph
    """

class param(HTMLTag):
    """
    Defines a parameter for an object
    """

class picture(HTMLTag):
    """
    Defines a container for multiple image resources
    """

class pre(HTMLTag):
    """
    Defines preformatted text
    """

class progress(HTMLTag):
    """
    Represents the progress of a task
    """

class q(HTMLTag):
    """
    Defines a short quotation
    """

class rp(HTMLTag):
    """
    Defines what to show in browsers that do not support ruby annotations
    """

class ruby(HTMLTag):
    """
    Defines a ruby annotation (for East Asian typography)
    """

class s(HTMLTag):
    """
    Defines text that is no longer correct
    """

class samp(HTMLTag):
    """
    Defines sample output from a computer program
    """

class script(HTMLTag):
    """
    Defines a client-side script
    """

class section(HTMLTag):
    """
    Defines a section in a document
    """

class select(HTMLTag):
    """
    Defines a drop-down list
    """

class small(HTMLTag):
    """
    Defines smaller text
    """

class source(HTMLTag):
    """
    Defines multiple media resources for media element (<video> and <audio>)
    """

class span(HTMLTag):
    """
    Defines a section in a document
    """

class strike(HTMLTag):
    """
    Defines strikethrough text

    Not supported in HTML5.
    Use <del> or <s> instead.
    """

class strong(HTMLTag):
    """
    Defines important text
    """

class style(HTMLTag):
    """
    Defines style information for a document
    """

class sub(HTMLTag):
    """
    Defines subscripted text
    """

class summary(HTMLTag):
    """
    Defines a visible heading for a <details> element
    """

class sup(HTMLTag):
    """
    Defines superscripted text
    """

class svg(HTMLTag):
    """
    Defines a container for SVG graphics
    """

class table(HTMLTag):
    """
    Defines a table
    """

class tbody(HTMLTag):
    """
    Groups the body content in a table
    """

class td(HTMLTag):
    """
    Defines a cell in a table
    """

class template(HTMLTag):
    """
    Defines a container for content that should be hidden when the page loads
    """

class textarea(HTMLTag):
    """
    Defines a multiline input control (text area)
    """

class tfoot(HTMLTag):
    """
    Groups the footer content in a table
    """

class th(HTMLTag):
    """
    Defines a header cell in a table
    """

class thead(HTMLTag):
    """
    Groups the header content in a table
    """

class time(HTMLTag):
    """
    Defines a specific time (or datetime)
    """

class title(HTMLTag):
    """
    Defines a title for the document
    """

class tr(HTMLTag):
    """
    Defines a row in a table
    """

class track(HTMLTag):
    """
    Defines text tracks for media elements (<video> and <audio>)
    """

class tt(HTMLTag):
    """
    Defines teletype text

    Not supported in HTML5. Use CSS instead.
    """

class ul(HTMLTag):
    """
    Defines an unordered list
    """

class var(HTMLTag):
    """
    Defines a variable
    """

class video(HTMLTag):
    """
    Defines embedded video content
    """

class wbr(HTMLTag):
    """
    Defines a possible line-break
    """

