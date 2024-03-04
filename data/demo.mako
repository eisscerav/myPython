hello, ${name}
pythagorean theorem:  ${pow(x,2) + pow(y,2)}

${"this is some text" | u}

% if x==5:
    this is some output when x==5
% endif

% if mylist:
% for i in mylist:
    <h5>${i['comp']}, ${i['val']}</h5>
% endfor
% endif

% for a in ['one', 'two', 'three', 'four', 'five']:
    % if a[0] == 't':
    its two or three
    % elif a[0] == 'f':
    four/five
    % else:
    one
    % endif
% endfor

%% some text
    %% some more text

<ul>
% for a in ("one", "two", "three"):
    <li>Item ${loop.index}: ${a}</li>
% endfor
</ul>

## this is a comment.
<%doc>
    these are comments
    more comments
</%doc>

here is a line that goes onto \
another line.

## demo python block
<%
    z = []
    for i in range(5):
        z.append(i**2)
%>
% for b in z:
    ${b}
% endfor

## demo def tag
<%def name="myfunc(x)">
    this is myfunc, x is ${x}
</%def>
${myfunc(7)}

## demo passing dict to template and how to use it
<h2>${my_company['company']}, ${my_company['value']}</h2>

## demo how to pass and use class in template
<h3>${person.name}, ${person.age}</h3>
<h5>person.name, person.age</h5>