
<h1> ${date}:</h1>
<h2>monthly job group by website</h2>
<table cellpadding="1" cellspacing="0" width="100%" border="1">
    <tr bgcolor="silver">
    <th align=center>website</th>
    <th align=center>number</th>

    </tr>

<% i = 0 %>
% for item in data:
    <tr>
        <td align=center>${item[0]}</td>
        <td align=center>${item[1]}</td>
    </tr>
%endfor
</table>


