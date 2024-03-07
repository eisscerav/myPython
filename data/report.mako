<!DOCTYPE html>
<html lang="en">
<head>
    <title>Coverity Report</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://unpkg.com/bootstrap-table@1.22.0/dist/bootstrap-table.min.css">

    <style>
        .table-green {
            background: #00ad27;
            color: #ffffff;
        }
        .my_caption-top {
            caption-side: top;
        }
    </style>
</head>
<body>
    <div class="container_non">
        <h1 class="table-green text-center">Coverity Report for ${project_name}</h1>
        <ul>
            <li><span class="table-green">Details without similar items</span></li>
        </ul>
        <table id="sanity_report" class="table table-striped table-bordered">
        <caption class="my_caption-top">Original report <a target="_blank" href=${original_link}><i class="fa fa-info-circle"></i></a></caption>
            <thead class="thead-light">
                <tr>
                    <th data-sortable="true"><b>Index</b></th>
                    <th data-sortable="true"><b>Original ID</b></th>
                    <th data-sortable="true"><b>File</b></th>
                </tr>
            </thead>
            <tbody>
                % for td_item in td_items:
                <tr>
                    <td>${loop.index+1}</td>
                    <td>${td_item['ID']}</td>
                    <td><a target="_blank" href=${td_item['file_href']}>${td_item['File']}</a></td>
                </tr>
                % endfor
            </tbody>
        </table>
    </div>

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
            integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
            crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.3/dist/umd/popper.min.js"
            integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49"
            crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/js/bootstrap.min.js"
            integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy"
            crossorigin="anonymous"></script>
    <script src="https://unpkg.com/bootstrap-table@1.22.0/dist/bootstrap-table.min.js"></script>
    <script>
        $(function () {
            $('#sanity_report').bootstrapTable({
                pageSize: 10,
                search: true,
                smartDisplay: true,
            });
        });
    </script>
</body>
</html>