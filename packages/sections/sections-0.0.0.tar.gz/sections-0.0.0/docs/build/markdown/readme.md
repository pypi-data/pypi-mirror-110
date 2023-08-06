# [ s e | c t | i o | n s ]

<!-- start-badges -->
[

![image](https://coveralls.io/repos/trevorpogue/sections/badge.svg?branch=master&service=github)

](https://coveralls.io/r/trevorpogue/sections) [

![image](https://img.shields.io/pypi/v/sections.svg)

](https://pypi.org/project/sections) [

![image](https://img.shields.io/pypi/pyversions/sections.svg)

](https://pypi.org/project/sections)

<!-- end-badges -->
Flexible tree data structures for organizing lists and dicts into sections.

sections is designed to be:


* **Intuitive**: Start quickly and spend less time reading the docs.


* **Scalable**: Grow arbitrarily complex trees as your problem scales.


* **Flexible**: Rapidly build nodes with any custom attributes, properties, and methods on the fly.


* **Fast**: Made with performance in mind - access lists and sub-lists/dicts in as little as Θ(1) time in many cases. See the Performance section for the full details.


* **Reliable**: Contains an exhaustive test suite and 100% code coverage.

## Documentation

[https://sections.readthedocs.io/](https://sections.readthedocs.io/)

## Usage

```
pip install sections
```

```
    import sections

    menu = sections(
        'Breakfast', 'Dinner',
        mains=['Bacon&Eggs', 'Burger'],
        sides=['HashBrown', 'Fries'],
    )
    # Resulting structure's API and the expected results
    assert menu.mains == ['Bacon&Eggs', 'Burger']
    assert menu.sides == ['HashBrown', 'Fries']
    assert menu['Breakfast'].main == 'Bacon&Eggs'
    assert menu['Breakfast'].side == 'HashBrown'
    assert menu['Dinner'].main == 'Burger'
    assert menu['Dinner'].side == 'Fries'
    assert menu('sides', dict) == {'Breakfast': 'HashBrown', 'Dinner': 'Fries'}
    assert isinstance(menu, sections.Section)
    assert isinstance(menu['Breakfast'], sections.Section)
    assert isinstance(menu['Dinner'], sections.Section)
```

### Attrs: Plural/singular hybrid attributes and more

Waste less time deciding between using the singular or plural form for an attribute name:

```
tasks = sections('pay bill', 'clean', status=['completed', 'started'])
assert tasks.statuses == ['completed', 'started']
assert tasks['pay bill'].status == 'completed'
assert tasks['clean'].status == 'started'
```

When an attribute is not found in a Section node, both the plural and singular forms of the word are then checked to see if the node contains the attribute under those forms of the word. If they are still not found, the node will recursively repeat the same search on each of its children, concatenating the results into a list or dict.

#### Properties: Easily add on the fly

Properties and methods are automatically added to a Section class instance when passed as keyword arguments:

```
    schedule = sections(
        'Weekdays', 'Weekend',
        hours_per_day=[[8, 8, 6, 10, 8], [4, 6]],
        hours=property(lambda self: sum(self.hours_per_day)),
    )
    assert schedule['Weekdays'].hours == 40
    assert schedule['Weekend'].hours == 10
    assert schedule.hours == 50
```

Each sections() call returns a structure containing nodes of a unique class created in a factory function, where the class definition contains no logic except that it inherits from the Section class. This allows properties added to one structure creation to not affect the class instances in other structures.

#### Construction: Build gradually or all at once

Construct in multiple possible way:

```
    def demo_different_construction_techniques():
        """Example construction techniques for producing the same structure."""
        # Building section-by-section
        books = sections()
        books['LOTR'] = sections(topic='Hobbits', author='JRR Tolkien')
        books['Harry Potter'] = sections(topic='Wizards', author='JK Rowling')
        demo_resulting_object_api(books)
        # Section-wise construction
        books = sections(
            sections('LOTR', topic='Hobbits', author='JRR Tolkien'),
            sections('Harry Potter', topic='Wizards', author='JK Rowling')
        )
        demo_resulting_object_api(books)
        # Attribute-wise construction
        books = sections(
            'LOTR', 'Harry Potter',
            topics=['Hobbits', 'Wizards'],
            authors=['JRR Tolkien', 'JK Rowling']
        )
        demo_resulting_object_api(books)
        # setattr post-construction
        books = sections(
            'LOTR', 'Harry Potter',
        )
        books.topics = ['Hobbits', 'Wizards']
        setattr(books, 'topics', ['Hobbits', 'Wizards'])
        books['LOTR'].author = 'JRR Tolkien'
        books['Harry Potter'].author = 'JK Rowling'
        demo_resulting_object_api(books)

    def demo_resulting_object_api(books):
        """Example Sections API and expected results."""
        assert books.names == ['LOTR', 'Harry Potter']
        assert books.topics == ['Hobbits', 'Wizards']
        assert books.authors == ['JRR Tolkien', 'JK Rowling']
        assert books['LOTR'].topic == 'Hobbits'
        assert books['LOTR'].author == 'JRR Tolkien'
        assert books['Harry Potter'].topic == 'Wizards'
        assert books['Harry Potter'].author == 'JK Rowling'

    demo_different_construction_techniques()
```

## Details

### Section Names

The non-keyword arguments passed into a sections() call define the section names and are accessed through the attribute name. The names are used like keys in a dict to access each child section of the root Section object:

```
    books = sections(
        'LOTR', 'Harry Potter',
        topics=['Hobbits', 'Wizards'],
        authors=['JRR Tolkien', 'JK Rowling']
    )
    assert books.names == ['LOTR', 'Harry Potter']
    assert books['LOTR'].name == 'LOTR'
    assert books['Harry Potter'].name == 'Harry Potter'
```

A parent section name can optionally be provided as the first argument in a list or Section instantiation by defining it in a set (surrounding it with curly brackets). This strategy avoids an extra level of braces when instantiating Sections. This idea applies also for defining the parent attributes:

```
    library = sections(
        {"Trevor's Bookshelf"},
        [{'Fantasy'}, 'LOTR', 'Harry Potter'],
        [{'Academic'}, 'Advanced Mathematics', 'Physics for Engineers'],
        topics=[[{'Imaginary things'}, 'Hobbits', 'Wizards'],
                [{'School'}, 'Numbers', 'Forces']],
    )
    assert library.name == "Trevor's Bookshelf"
    assert library.sections.names == ['Fantasy', 'Academic']
    assert library['Fantasy'].sections.names == ['LOTR', 'Harry Potter']
    assert library['Academic'].sections.names == [
        'Advanced Mathematics', 'Physics for Engineers'
    ]
    assert library['Fantasy']['Harry Potter'].name == 'Harry Potter'
    assert library['Fantasy'].topic == 'Imaginary things'
    assert library['Academic'].topic == 'School'
```

### Subclassing

Inheriting Section is easy, the only requirement is to call super().__init__(

```
*
```

args, 

```
**
```

kwds) at some point in __init__  like below if you override that method:

```
    class Library(sections.Section):
        def __init__(price="Custom default value", **kwds):
            super().__init__(**kwds)

        @property
        def genres(self):
            if self.isroot:
                return self.sections
            else:
                raise AttributeError('This library has only 1 level of genres')

        @property
        def books(self): return self.leaves

        @property
        def titles(self): return self.names

        def critique(self, impression="Haven't read it yet", rating=0):
            self.review = impression
            self.price = rating * 2

    library = Library(
        [{'Fantasy'}, 'LOTR', 'Harry Potter'],
        [{'Academic'}, 'Advanced Math.', 'Physics for Engineers']
    )
    assert library.genres.names == ['Fantasy', 'Academic']
    assert library.books.titles == [
        'LOTR', 'Harry Potter', 'Advanced Math.', 'Physics for Engineers'
    ]
    library.books['LOTR'].critique(impression='Good but too long', rating=7)
    library.books['Harry Potter'].critique(
        impression="I don't like owls", rating=4)
    assert library.books['LOTR'].price == 14
    assert library.books['Harry Potter'].price == 8
    import pytest
    with pytest.raises(AttributeError):
        this_should_raise_error = library['Fantasy'].genres
```

Section.__init__ assigns the kwds values passed to it to the object attributes, and the passed kwds are generated during instantiation by a metaclass.

### Performance

Each non-leaf Section node keeps a cache containing quickly-readable references to an attribute dict previously parsed from manual traversing through descendant nodes in a previous read. The caches are invalidated when the tree structure or node attribute values change. The caches allow instant reading of sub lists/dicts in Θ(1) time and can often make structure attribute reading faster by 5x and even much more. The downside is that it also increases memory used by roughly 5x as well. This is not a concern on a general-purpose computer for structures containing less than 1000 - 10,000 nodes. For clarity, converting a list with 10,000 elements would create 10,001 nodes (1 root plus 10,000 children). After 10,000 nodes, it may be recommended to consider changing the node or structure’s class attribute use_cache to 

```
`
```

False’. This can be done as follows:

```
    sect = sections([42] * (10 ** 4))
    sect.cls.use_cache = False          # turn off for all nodes in `sect`
    sect.use_cache = False              # turn off for just the root node
    sections.Section.use_cache = False  # turn off for all future structures
```

## Development

To run all the tests run:

```
tox
```

Note, to combine the coverage data from all the tox environments run:

| Windows

 | ```
set PYTEST_ADDOPTS=--cov-append
tox
```

 |
| Other

   | ```
PYTEST_ADDOPTS=--cov-append tox
```

     |
