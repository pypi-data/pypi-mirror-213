from enum import StrEnum


# Categories of events used were found at W3Schools.com
# https://www.w3schools.com/tags/ref_eventattributes.asp
# 
# For an enumerator with all event attributes, use Event.


WindowEvent = StrEnum('WindowEvent', (
    'onafterprint',
    'onbeforeprint',
    'onbeforeunload',
    'onerror',
    'onhashchange',
    'onload',
    'onmessage',
    'onoffline',
    'ononline',
    'onpagehide',
    'onpageshow',
    'onpopstate',
    'onresize',
    'onstorage',
    'onunload',
))


FormEvent = StrEnum('FormEvent', (
    'onblur',
    'onchange',
    'oncontextmenu',
    'onfocus',
    'oninput',
    'oninvalid',
    'onreset',
    'onsearch',
    'onselect',
    'onsubmit',
))


KeyboardEvent = StrEnum('KeyboardEvent', (
    'onkeydown',
    'onkeypress',
    'onkeyup',
))


MouseEvent = StrEnum('MouseEvent', (
    'onclick',
    'ondblclick',
    'onmousedown',
    'onmousemove',
    'onmouseout',
    'onmouseover',
    'onmouseup',
    'onmousewheel',
    'onwheel',
))

DragEvent = StrEnum('DragEvent', (
    'ondrag',
    'ondragend',
    'ondragenter',
    'ondragleave',
    'ondragover',
    'ondragstart',
    'ondrop',
    'onscroll',
))

ClipboardEvent = StrEnum('ClipboardEvent', (
    'oncopy',
    'oncut',
    'onpaste',
))


MediaEvent = StrEnum('MediaEvent', (
    'onabort',
    'oncanplay',
    'oncanplaythrough',
    'oncuechange',
    'ondurationchange',
    'onemptied',
    'onended',
    'onerror',
    'onloadeddata',
    'onloadedmetadata',
    'onloadstart',
    'onpause',
    'onplay',
    'onplaying',
    'onprogress',
    'onratechange',
    'onseeked',
    'onseeking',
    'onstalled',
    'onsuspend',
    'ontimeupdate',
    'onvolumechange',
    'onwaiting',
))


MiscEvent = StrEnum('MiscEvent', (
    'ontoggle',
))


# Create one enumerator with the superset of
# all attributes of the different categories.

types = { WindowEvent, FormEvent, KeyboardEvent,
          MouseEvent, DragEvent, ClipboardEvent,
          MediaEvent, MiscEvent }

Event = StrEnum('Event', [*{
    event
    for event_type in types
    for event in event_type.__members__.keys()
}])
