import json
import requests
from datetime import datetime, timedelta

class FinanceAPITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1/finance"
        
    def test_endpoint(self, endpoint, method="GET", data=None):
        """Test a specific API endpoint"""
        url = f"{self.api_url}/{endpoint}/"
        
        try:
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                response = requests.post(url, json=data)
            
            print(f"\n{method} {endpoint}/")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if isinstance(result, dict) and 'results' in result:
                        print(f"Count: {result.get('count', 0)}")
                        print(f"Sample data: {json.dumps(result['results'][:2], indent=2)}")
                    else:
                        print(f"Data: {json.dumps(result[:2] if isinstance(result, list) else result, indent=2)}")
                except:
                    print("Response is not JSON")
            else:
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"Error testing {endpoint}: {str(e)}")
    
    def run_comprehensive_test(self):
        """Run tests for all finance endpoints"""
        print("=== FINANCE API COMPREHENSIVE TEST ===")
        print(f"Testing API at: {self.api_url}")
        
        # Test all main endpoints
        endpoints = [
            "currencies",
            "account-types", 
            "accounts",
            "vendors",
            "customers",
            "invoices",
            "expenses",
            "expense-categories",
            "budgets",
            "budget-categories",
            "journal-entries",
            "financial-forecasts",
            "anomaly-detections",
            "tax-authorities",
            "tax-rates"
        ]
        
        for endpoint in endpoints:
            self.test_endpoint(endpoint)
        
        # Test special AI endpoints
        print("\n=== TESTING AI-POWERED ENDPOINTS ===")
        
        # Test currency exchange rate update
        self.test_endpoint("currencies/1/update_exchange_rates", "POST")
        
        # Test financial forecasting
        print("\nTesting Financial Forecasting...")
        forecast_data = {
            "forecast_type": "REVENUE",
            "period_days": 30
        }
        self.test_endpoint("financial-forecasts/generate_forecast", "POST", forecast_data)
        
        # Test anomaly detection
        print("\nTesting Anomaly Detection...")
        self.test_endpoint("anomaly-detections/detect_anomalies", "POST")
        
        # Test budget variance analysis
        print("\nTesting Budget Variance Analysis...")
        self.test_endpoint("budgets/1/variance_analysis")
        
        # Test invoice aging report
        print("\nTesting Invoice Aging Report...")
        self.test_endpoint("invoices/aging_report")
        
        print("\n=== TEST COMPLETED ===")

if __name__ == "__main__":
    tester = FinanceAPITester()
    tester.run_comprehensive_test()
