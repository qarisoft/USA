# Set-ExecutionPolicy -ExecutionPolicy Bypass
try {
    .env/Scripts/activate
    .env/Scripts/python.exe .\manage.py runserver
    Start-Process  http://127.0.0.1:8000
}
catch {
    "somthing wrong"
    # ./main.ps1
    # .env/Scripts/activate
    # .env/Scripts/python.exe .\manage.py runserver
    # py .\manage.py runserver
    <#Do this if a terminating exception happens#>
}