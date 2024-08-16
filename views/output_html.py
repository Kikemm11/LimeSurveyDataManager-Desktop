html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Survey Responses</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    
    <style>
        table {
            table-layout: auto; 
            width: 100%; 
        }
        th, td {
            text-align: center; 
            white-space: nowrap; 
            padding: 8px; 
        }
        th {
            white-space: nowrap; 
            font-weight: bold; 
        }
        td {
            white-space: normal; 
        }
    </style>
  
</head>
<body>
    <div class="container">
         <h1 class="text-center mb-5 mt-4">Survey Responses</h1>

        <div class="table-container">
            <table class="table mt-3">
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
    </div>
</body>
</html>
"""