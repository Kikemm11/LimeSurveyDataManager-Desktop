html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Survey Responses</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <link rel="stylesheet" href="styles.css">
    
</head>
<body>
    <div class="container">
         <h1 class="text-center mb-5 mt-4">Survey Responses</h1>

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

        // Initialize the first page
        showPage(currentPage);
    </script>

</body>
</html>
"""