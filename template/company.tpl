
<h1> ${date}:</h1>
<h2>total jobs:${total}</h2>
<table cellpadding="1" cellspacing="0" width="100%" border="1">
    <tr bgcolor="silver">
    <th align=center>id</th>
    <th align=center>name</th>

    </tr>

<% i = 0 %>
% for item in data:
    <% i += 1%>
    <tr>
        <td align=center>${i}</td>
        <td align=center></td>
    </tr>
%endfor
</table>


