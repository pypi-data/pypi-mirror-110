# Reference


* sections


This part of the documentation covers the main sections class representing each node object in a tree structure and all of its interfaces.

<!-- Main Interface
-------------- -->
<!-- Classes
------- -->

### class sections.Section(\*args: NewType.<locals>.new_type, parent: NewType.<locals>.new_type = None, \*\*kwds: NewType.<locals>.new_type)
Objects instantiated by `Section` are nodes in a sections
tree structure. Each node has useful methods and properties for organizing
lists/dicts into sections and for conveniently accessing/modifying the
sub-list/dicts from each section/subsection.


#### \__call__(name: str, gettype: NewType.<locals>.new_type = 'default')
Run `get_nearest_attr`. This returns
attribute name from self if self contains the attribute in either the
singular or plural form for name. Else, try the same pattern for each
of self’s children, putting the returned results from each child into a
list. Else, raise AttributeError.


* **Parameters**

    
    * **name** – The name of the attribute to find in self or self’s
    descendants


    * **gettype** – Valid values are list, iter, dict, ‘full_dict’.
    Setting to list returns a list containing the
    attribute values.
    Setting to iter returns an iterable iterating
    through the attribute
    values. Setting to dict returns a dict containing
    pairs of the
    containing node’s name with the attribute value.
    Setting to
    ‘full_dict’ is faster than dict and returns a
    dict containing pairs
    of a reference to each node and its attribute value.
    ‘full_dict’
    output is visually identical to dict for printing
    purposes, but it
    will contain all attributes even if some source nodes
    have duplicate
    names. The only downside to ‘full_dict’ that the
    keys cannot be
    referenced by name like with dict, but all values()
    are still valid.



* **Returns**

    The attribute name of self if present, else an iterable
    object containing the attribute name formed from the nearest
    relatives of self. The type of the iterable object depends
    on gettype.



#### \__getattr__(name: str)
Called if self node does not have attribute name, in which case try
finding attribute name from :meth: __call__ <Section.__call__>.


#### \__getitem__(name: Any)
Return child node name of self.


#### \__iter__()
By default iterate over child nodes instead of their names/keys.


#### \__setattr__(name: str, value: Any, _invalidate_cache=True)
If value is a list, recursively
setattr for each child node with the corresponding value element from
the value list.


#### \__setitem__(name: Any, value: Union[NewType.<locals>.new_type, NewType.<locals>.new_type])
Add a child name to self. Ensure added children are converted to the
same unique Section type as the rest of the nodes in the structure, and
update its name to name, and its parent to self.


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
