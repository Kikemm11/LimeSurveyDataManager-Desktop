

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Survey Responses</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
</head>
<body>
    <div class="container">
        <h1>Survey Responses</h1>

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
                                {% if 'Foto' not in col %}
                                    <td>{{ output_df.iloc[i][col] }}</td>
                                {% else %}
                                    {% if img_dict.get(output_df.iloc[i][col]) %}
                                        <td><img src="{{ img_dict.get(output_df.iloc[i][col]) }}"  width="100" height="100"></td>
                                    {% else %}
                                        <td>{{ output_df.iloc[i][col] }}</td>
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