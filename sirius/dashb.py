import mysql.connector
import plotly.graph_objs as go
cnx = mysql.connector.connect(user='root', password='waad',
                              host='localhost',
                              database='crypto')


cursor = cnx.cursor()
query = ("SELECT number, hash, nonce "
         "FROM blockchain "
         "ORDER BY number")
cursor.execute(query)

transaction_history = []
for (number, hash, nonce) in cursor:
    transaction_history.append({'number': number,
                                'hash': hash,
                                'nonce': nonce})

# Create a list of x values (transaction order)
x_values = list(range(1, len(transaction_history) + 1))

# Create a list of y values (nonce)
y_values = [t['nonce'] for t in transaction_history]

# Create a scatter plot using Plotly
fig = go.Figure(data=go.Scatter(x=x_values, y=y_values, mode='markers'))
fig.update_layout(title='Transaction History', xaxis_title='Transaction Order', yaxis_title='Nonce')

# Display the scatter plot
fig.show()