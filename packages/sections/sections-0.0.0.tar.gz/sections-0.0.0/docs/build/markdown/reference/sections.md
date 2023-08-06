# sections

<!-- from sections import * -->
Flexible tree data structures for organizing lists and dicts into sections.

github.com/trevorpogue/sections


### class sections.MetaSection()
Parses args and kwds passed to a sections() call or `Section` instantiation and returns a Section tree structure. Parses
node names/keys, separate attrs intended for current node vs child nodes,
constructs current node, then recursively repeats for all child nodes.


### class sections.Section(\*args: NewType.<locals>.new_type, parent: NewType.<locals>.new_type = None, \*\*kwds: NewType.<locals>.new_type)
Objects instantiated by `Section` are nodes in a sections
tree structure. Each node has useful methods and properties for organizing
lists/dicts into sections and for conveniently accessing/modifying the
sub-list/dicts from each section/subsection.


#### property children()
Get self nodes’s children.
Returns a Section node that has no public attrs and has shallow copies
of self node’s children as its children. This can be useful if self has
an attr attr but you want to access a list of the childrens’ attr
attr, then write section.children.attr to access the attr list.


#### property cls()
The unique structure-wide class of each node.


#### deep_str(breadthfirst: bool = True, _topcall: bool = True)
Print the output of 

```
:met:`node_str <Section.node_str`
```

 for self and all
of its descendants.


#### default_gettype()
alias of `builtins.list`


#### property entries()
leaves <Section.leaves>.


* **Type**

    A synonym for



* **Type**

    meth



#### get_nearest_attr(name: str, gettype: NewType.<locals>.new_type = 'default')
Default method called by `__call__`. See
the docstring of `__call__` for the full
details. :meta private:


#### get_node_attr(name: str, gettype: NewType.<locals>.new_type = 'default')
Return attribute name only from self as opposed to searching for
attribute attr in descendant nodes as well.


#### property ischild()
True iff self node has a parent.


#### property isleaf()
True iff self node has no children.


#### property isparent()
True iff self node has any children.


#### property isroot()
True iff self node has not parent.


#### property leaves()
Get all leaf node descendants of self.
Returns a Section node that has no public attrs and has shallow copies
of self node’s leaves as its children. This can be useful if self has
an attr attr but you want to access a list of the leaves’ attr
attr, then write section.leaves.attr to access the leaf attr list.


#### property leaves_iter()
Return iterator that iterates through all self’s leaf node descendants.


#### node_str()
Neatly print the public attributes of the Section node and its class,
as well as its types property output.


#### node_withchildren_fromiter(itr: iter)
Perform a general form of the task performed in :meth:leaves
Section.leaves. Return a Section node with any children referenced
in the iterable from the itr argument.


#### property nofchildren()
Nunber of children Sections/nodes.


#### pop(name: Any)
Remove child name from self.


#### popitem()
Remove last added child from self.


#### property sections()
children <Section.chldren>.


* **Type**

    A synonym for



* **Type**

    meth



#### setdefault(\*args: Any, \*\*kwds: Any)
Not supported yet. :meta private:


#### update(\*args: Any, \*\*kwds: Any)
Invalidate descendant attr cache after adding/removing nodes.
:meta private:
