"""
Application Entry Point
Run this file to start the Timesheet Validator application
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("Starting Timesheet Validator Application")
    print("=" * 60)
    print("\nApplication Information:")
    print(f"   - Server: http://localhost:5000")
    print(f"   - Environment: Development")
    print(f"   - Debug Mode: Enabled")
    print("\nInstructions:")
    print("   1. Open your browser and go to http://localhost:5000")
    print("   2. Select your team from the dropdown")
    print("   3. Upload your timesheet and ticket data files")
    print("   4. Click 'Validate Timesheet' to process")
    print("   5. Download the results Excel file")
    print("\nPress CTRL+C to stop the server")
    print("=" * 60)
    print()
    
    app.run(debug=False, host='0.0.0.0', port=5000)

# Made with Bob
