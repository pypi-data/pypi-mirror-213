# Domini

A small, simple package for generating HTML documents.
The syntax aims to immitate HTML as closely as possible for legibility and easy of use.

### Index

- [Attributes](#attributes)
- [Content](#content)
- [Extras](#extras)

## Attributes

Attributes *without* a value are entered as *positional arguments*.<br>
Attributes *with* a value are entered as *keyword arguments*.

To specify attributes that collide with reserved Python keywords,
append an underscore and it will be removed.

#### Python

```py
from domini.html import dialog

dialog('open', class_='mydialog')
```

#### HTML

```html
<dialog open class='mydialog'>
```

## Content

To add children to an element, you can use either the `add` method or the short-hand greater-than operator. The right-hand side can be either an iterable or a lone element. These elements can be either other tags or plain strings.

**NOTE**: `add` does add them to the current object. `>` returns a new, identical element with those children added.

```py
ul(class_='todo')> (
    li()> 'Buy a fruit basket.',
    li()> (
        'Read ', a(href='https://wikipedia.org/')> 'Wikipedia',
        ' to learn more about things you may not have otherwise cared about.',
    ),
)
```

## Closing tags

A tag is only closed if content is provided. E.g. `<p></p>` as opposed to `<p>`. This can be an empty tuple.

```py
p()> ()
```

For open tags like `<br>` and `<hr>`, you simply do `br()` and `hr()`.

## Extras

These are small, miscellaneous additions that can be useful but don't really serve any wider purpose within the context of the package itself. Though this might change in the future.

### Event attributes

Enumerators for event attributes are available at `domini.html.events`. You can either use `Event`, which contains all different event attributes in one, or use an enumerator for a specific category of events.

```py
from domini.html.events import (
    # These are the categories.
    WindowEvent, FormEvent, KeyboardEvent,
    MouseEvent, DragEvent, ClipboardEvent,
    MediaEvent, MiscEvent,
)
```
