template_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Survey Responses</title>
    <link rel="icon" href="{{ img_path }}" type="image/x-icon">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>

        /*Main body style*/

        body {
            margin: 0;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(to right, #F0FFF0, #E0F8E0) no-repeat center center fixed;
            position: relative;
            font-family: 'Poppins', sans-serif;
        }

        /*Statistics button style*/

        #statisticsButton {
            position: absolute;
            top: 50px;
            right: 5%;
            background-color: #ABD148;
            border: none;
            border-radius: 10px;
            padding: 20px 40px;
            font-family: 'Poppins', sans-serif;
            font-size:large; 
            font-weight: bold; 
            color: black;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        #statisticsButton:hover {
            background-color: #F3FAB3; 
        }

        /*Main container style*/

        .container-response {
            padding: 5px; 
            margin: 5px; 
            max-width: 100%; 
        }
        .title {
            display: flex;
            justify-content: flex-start; 
            margin: 1.2rem 0 1.5rem 0.5rem; 
            font-family: 'Poppins', sans-serif; 
            color: #79C557; 
            font-weight: 900; 
            font-size: 4rem;
        }
        .svg-icon {
            width: 130px;  
            height: 130px;  
            vertical-align: middle; 
            margin: 0.5rem 0 0.4rem 0.4rem; 
        } 
        .table-container {
            width: 100%; 
            margin: 0; 
            padding: 0; 
        }
        table {
            table-layout: auto; 
            width: 100%;
            border-collapse: collapse; 
            border: 2px solid #363636;
            font-family: 'Poppins', sans-serif;    
        }
        th, td {
            text-align: center; 
            white-space: nowrap; 
            padding: 8px;
            font-family: 'Poppins', sans-serif; 
        }
        th {
            white-space: nowrap;
            font-size: 1.2rem; 
            font-weight: bold;
            background-color: #32CD32;
            color: white; 
        }
        td {
            white-space: normal;
            font-size: 1rem; 
        }
        tbody tr:nth-child(odd) {
            background-color: #c5faadab; 
            color: black; 
        }
        tbody tr:nth-child(even) {
            background-color: #c6faad;
            color: black; 
        }
        .pagination {
            display: flex;
            justify-content: center; 
            align-items: center; 
            margin-top: 12px; 
            padding: 0; 
        }
        .pagination button {
            background-color: #79C557; 
            border: none;
            border-radius: 20px; 
            padding: 15px 30px; 
            font-family: 'Poppins', sans-serif; 
            font-weight: bold; 
            color: black; 
            cursor: pointer;
            transition: background-color 0.3s ease; 
            margin: 0 10px 0 0; 
        }
        .pagination button:hover {
            background-color: #F3FAB3; 
        }
        .pagination button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }    

        /*Statistics container style*/

        .container-statistics {
            padding: 20px;
            margin: 0;
            width: 100%;
            display: flex;
            flex-direction: column; 
        }
        .hidden {
            display: none;
        }
        .titleSt-container {
            display: flex;
            align-items: center;
            margin-bottom: 50px; 
        }
        .title-statistics {
            display: flex;
            justify-content: flex-start; 
            margin: 1.2rem 0 1.5rem 0.5rem; 
            font-family: 'Poppins', sans-serif; 
            color: #79C557; 
            font-weight: 900; 
            font-size: 4rem;
        }
        .svg-icon-statistics {
            width: 130px;
            height: 130px;
        }    
        .charts-container {
            display: flex;
            flex-wrap: wrap; 
            gap: 40px; 
        }
        .charts {
            font-family: 'Poppins', sans-serif;
            flex: 1 1 calc(50% - 20px); 
            min-width: 300px;
            box-sizing: border-box;
            max-width: 920px;
            margin-bottom: 30px;  
        }   
    </style>
</head>
<body>

    <button id="statisticsButton" onclick="toggleView()">Statistics</button>

    <div class="container-response">
        <div class="title">
            <h1 class="title">Survey Responses</h1>
            <img src="{{ img_path }}" alt="SVG Image" class="svg-icon">
        </div>        
        <div class="table-container">
            <table class="table mt-3" id="surveyTable">
                <thead class="thead-dark">
                    <tr>
                        {% for name in column_names %}
                        <th>{{ name }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody>
                    {% for i in range(df_lenght) %}
                        <tr>
                            {% for col in column_names %}    
                                {% if ('Foto' not in col) and ('Ubicación' not in col) %}
                                    <td>{{ output_df.iloc[i][col] }}</td>
                                {% else %}
                                    {% if 'Foto' in col %}
                                        {% if img_dict.get(output_df.iloc[i][col]) %}
                                            <td><img src="{{ img_dict.get(output_df.iloc[i][col]) }}"  width="100" height="100"></td>
                                        {% else %}
                                            <td>{{ output_df.iloc[i][col] }}</td>
                                        {% endif %}
                                    {% else %}
                                        <td>
                                            <a href="https://www.google.com/maps?q= {{ output_df.iloc[i][col] }}" target="_blank">
                                            <img src="https://img.icons8.com/ios-filled/50/000000/map-marker.png" alt="Map Icon" width="30" height="30">
                                        </td>    
                                    {% endif %}    
                                {% endif %}
                            {% endfor %}
                        </tr>
                    {% endfor %}

                </tbody>
            </table>
        </div>
        <div class="pagination">
            <button id="prevBtn" onclick="prevPage()" disabled>Previous</button>
            <button id="nextBtn" onclick="nextPage()">Next</button>
        </div>
    </div>

    <div class="container-statistics hidden">
        <div class="titleSt-container">
            <h1 class="title-statistics">Statistics</h1>
            <img src="{{ img_path }}" alt="SVG Image" class="svg-icon-statistics">
        </div>
        <div class="charts-container">
            {% for i in range(piechart_len) %}
                <div class="charts">
                    <h3>{{ piechart_options[i] }}</h3>
                    <div id="pie_chart{{i}}">
                        <canvas id="pie-chart{{i}}"></canvas>
                    </div>
                </div>
            {% endfor %}
        </div>
    </div>  
    <script>
        const rowsPerPage = 4;
        let currentPage = 1;
        const table = document.getElementById("surveyTable");
        const totalRows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr").length;
        const totalPages = Math.ceil(totalRows / rowsPerPage);

        function showPage(page) {
            const start = (page - 1) * rowsPerPage;
            const end = start + rowsPerPage;
            const rows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");

            for (let i = 0; i < totalRows; i++) {
                rows[i].style.display = (i >= start && i < end) ? '' : 'none';
            }

            document.getElementById("prevBtn").disabled = page === 1;
            document.getElementById("nextBtn").disabled = page === totalPages;
        }

        function prevPage() {
            if (currentPage > 1) {
                currentPage--;
                showPage(currentPage);
            }
        }

        function nextPage() {
            if (currentPage < totalPages) {
                currentPage++;
                showPage(currentPage);
            }
        }

        showPage(currentPage);
    </script>
    <script>
        function toggleView() {
            const responseContainer = document.querySelector('.container-response');
            const statisticsContainer = document.querySelector('.container-statistics');

            responseContainer.classList.toggle('hidden');
            statisticsContainer.classList.toggle('hidden');

            const button = document.getElementById("statisticsButton");
            if (responseContainer.classList.contains('hidden')) {
                button.textContent = "Survey Responses";
            } else {
                button.textContent = "Statistics";
            }
        }

        showPage(currentPage);
    </script>
    <script>

        var data = {{piechart_data}}
        let columns = [];
        let pieChartArray = [];
        let myPieChart;
    
        for (let key in data) {
            columns.push(key);
        }    

        for (var i = 0; i < columns.length; i++) {
            
            var col_name = columns[i];  
            var answers = data[col_name];

            var elementId = 'pie-chart' + i;

            var ctx1 = document.getElementById(elementId).getContext('2d');

            var chartType = Object.keys(answers).length < 5 ? 'pie' :  'bar';

            myPieChart = new Chart(ctx1, {
                type: chartType,
                data: {
                    datasets: [{
                        data: Object.entries(answers).map(([key, value]) => value),
                        backgroundColor: ['#F2AA33', '#1898D0 ', '#F5ED41', '#0A447D', '#7D0A55', '#E64646', '#69B05D', '#5DB0AB', '#AA5DB0']
                    }],
                    labels: Object.entries(answers).map(([key, value]) => key)
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: chartType == 'pie'
                        }
                    }
                    }
                }
            );

        }
    </script>
</body>
</html>
"""