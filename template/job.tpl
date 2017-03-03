
<h3> ${date}）</h3>
<table cellpadding="1" cellspacing="0" width="100%" border="1">
    <tr bgcolor="silver">
    <th align=center>id</th>
    <th align=center>title</th>
    <th align=center>company</th>
    <th align=center>link</th>

    </tr>

<% i = 0 %>
% for item in data_list:
    <% i += 1%>
    <tr>
        <td align=center>${i}</td>
        <td align=center>${item['title']}</td>
        <td align=center>${item['company']}</td>
        <td align=center>${item['link']}</td>
    </tr>
%endfor
</table>


