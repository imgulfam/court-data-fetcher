from app import create_app

# Create an instance of the app using our factory function
app = create_app()

if __name__ == '__main__':
    # The __name__ == '__main__' block ensures that the server is only run
    # when the script is executed directly.
    
    # app.run(debug=True) starts the Flask development server.
    # 'debug=True' is very useful during development because it automatically
    # reloads the server when you change a file and shows detailed errors.
    app.run(debug=True)