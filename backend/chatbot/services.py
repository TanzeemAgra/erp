"""
Smart Chatbot with RAG (Retrieval-Augmented Generation) Capabilities
Handles both Employee and Customer inquiries with contextual data retrieval
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q

# AI/ML imports
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document
import openai

# ERP Models
from accounts.models import User
try:
    from hr.models import Department, Employee
except ImportError:
    Department = None
    Employee = None

try:
    from assets.models import Asset, InventoryItem, Vendor
except ImportError:
    Asset = None
    InventoryItem = None
    Vendor = None

try:
    from crm.models import Customer
except ImportError:
    Customer = None

try:
    from projects.models import Project
except ImportError:
    Project = None

try:
    from finance.models import Invoice
except ImportError:
    Invoice = None

User = get_user_model()

class SmartChatbotService:
    """
    AI-Powered Chatbot with RAG capabilities for ERP system
    Features:
    - Employee assistance (HR, payroll, policies)
    - Customer support (orders, invoices, tracking)
    - Intelligent context retrieval from ERP data
    """
    
    def __init__(self):
        self.openai_api_key = getattr(settings, 'OPENAI_API_KEY', os.getenv('OPENAI_API_KEY'))
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in settings or environment.")
        
        openai.api_key = self.openai_api_key
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Initialize vector stores
        self.employee_vectorstore = None
        self.customer_vectorstore = None
        self.policy_vectorstore = None
        
        # Initialize RAG chains
        self.employee_qa_chain = None
        self.customer_qa_chain = None
        self.policy_qa_chain = None
        
        self._setup_vector_stores()
        self._setup_qa_chains()
    
    def _setup_vector_stores(self):
        """Setup vector stores for different data types"""
        try:
            # Employee data
            employee_docs = self._get_employee_documents()
            if employee_docs:
                self.employee_vectorstore = FAISS.from_documents(employee_docs, self.embeddings)
            
            # Customer data
            customer_docs = self._get_customer_documents()
            if customer_docs:
                self.customer_vectorstore = FAISS.from_documents(customer_docs, self.embeddings)
            
            # Company policies and documentation
            policy_docs = self._get_policy_documents()
            if policy_docs:
                self.policy_vectorstore = FAISS.from_documents(policy_docs, self.embeddings)
                
        except Exception as e:
            print(f"Error setting up vector stores: {e}")
    
    def _get_employee_documents(self) -> List[Document]:
        """Extract and format employee-related documents"""
        documents = []
        
        try:
            # Employee data
            if Employee:
                employees = Employee.objects.select_related('user', 'department', 'designation').all()
                for emp in employees:
                    doc_content = f"""
                    Employee: {emp.user.get_full_name()}
                    Employee ID: {emp.employee_id}
                    Department: {emp.department.name if emp.department else 'N/A'}
                    Designation: {emp.designation.title if emp.designation else 'N/A'}
                    Email: {emp.user.email}
                    Phone: {emp.phone}
                    Date Joined: {emp.date_joined}
                    Salary: {emp.salary}
                    Status: {'Active' if emp.is_active else 'Inactive'}
                    """
                    documents.append(Document(
                        page_content=doc_content,
                        metadata={
                            "type": "employee",
                            "employee_id": emp.employee_id,
                            "user_id": emp.user.id
                        }
                    ))
            
            # Department data
            if Department:
                departments = Department.objects.all()
                for dept in departments:
                    doc_content = f"""
                    Department: {dept.name}
                    Description: {dept.description}
                    Manager: {dept.manager.get_full_name() if dept.manager else 'No manager assigned'}
                    Employee Count: {dept.employees.count() if hasattr(dept, 'employees') else 0}
                    """
                    documents.append(Document(
                        page_content=doc_content,
                        metadata={"type": "department", "dept_id": dept.id}
                    ))
            
            # Assets data for employee reference
            if Asset:
                assets = Asset.objects.select_related('assigned_to', 'category', 'vendor').all()
                for asset in assets:
                    if asset.assigned_to:
                        doc_content = f"""
                        Asset: {asset.name}
                        Asset Tag: {asset.asset_tag}
                        Category: {asset.category.name}
                        Assigned to: {asset.assigned_to.get_full_name()}
                        Status: {asset.status}
                        Purchase Date: {asset.purchase_date}
                        Current Value: ${asset.current_value}
                        Location: {asset.location.name if asset.location else 'Not specified'}
                        """
                        documents.append(Document(
                            page_content=doc_content,
                            metadata={
                                "type": "asset",
                                "asset_id": asset.id,
                                "assigned_to": asset.assigned_to.id
                            }
                        ))
            
        except Exception as e:
            print(f"Error getting employee documents: {e}")
        
        return documents
    
    def _get_customer_documents(self) -> List[Document]:
        """Extract and format customer-related documents"""
        documents = []
        
        try:
            # Customer data
            if Customer:
                customers = Customer.objects.all()
                for customer in customers:
                    doc_content = f"""
                    Customer: {customer.name}
                    Company: {customer.company}
                    Email: {customer.email}
                    Phone: {customer.phone}
                    Address: {customer.address}
                    Customer Type: {customer.customer_type}
                    Status: {'Active' if customer.is_active else 'Inactive'}
                    Registration Date: {customer.created_at}
                    """
                    documents.append(Document(
                        page_content=doc_content,
                        metadata={"type": "customer", "customer_id": customer.id}
                    ))
            
            # Project data related to customers
            if Project:
                projects = Project.objects.select_related('client').all()
                for project in projects:
                    doc_content = f"""
                    Project: {project.name}
                    Client: {project.client.name if project.client else 'Internal'}
                    Description: {project.description}
                    Status: {project.status}
                    Start Date: {project.start_date}
                    End Date: {project.end_date}
                    Budget: ${project.budget}
                    Team Size: {project.team_members.count() if hasattr(project, 'team_members') else 0}
                    """
                    documents.append(Document(
                        page_content=doc_content,
                        metadata={
                            "type": "project", 
                            "project_id": project.id,
                            "client_id": project.client.id if project.client else None
                        }
                    ))
            
            # Invoice data
            if Invoice:
                invoices = Invoice.objects.select_related('client').all()
                for invoice in invoices:
                    doc_content = f"""
                    Invoice: {invoice.invoice_number}
                    Client: {invoice.client.name if invoice.client else 'N/A'}
                    Amount: ${invoice.total_amount}
                    Status: {invoice.status}
                    Due Date: {invoice.due_date}
                    Created: {invoice.created_at}
                    Description: {invoice.description}
                    """
                    documents.append(Document(
                        page_content=doc_content,
                        metadata={
                            "type": "invoice",
                            "invoice_id": invoice.id,
                            "client_id": invoice.client.id if invoice.client else None
                        }
                    ))
                
        except Exception as e:
            print(f"Error getting customer documents: {e}")
        
        return documents
    
    def _get_policy_documents(self) -> List[Document]:
        """Extract company policies and documentation"""
        documents = []
        
        # Default company policies (these would typically come from a database)
        policies = [
            {
                "title": "Leave Policy",
                "content": """
                Annual Leave: All employees are entitled to 21 days of annual leave per year.
                Sick Leave: 10 days of sick leave per year with medical certificate required for more than 2 consecutive days.
                Maternity/Paternity Leave: 12 weeks maternity leave, 2 weeks paternity leave.
                Emergency Leave: Up to 3 days for family emergencies.
                Application Process: Submit leave requests through HR portal at least 2 weeks in advance for annual leave.
                """
            },
            {
                "title": "Payroll Policy",
                "content": """
                Salary Payment: Salaries are paid on the last working day of each month.
                Overtime: Overtime is paid at 1.5x regular rate for hours exceeding 40 per week.
                Deductions: Standard deductions include income tax, social security, and health insurance.
                Bonuses: Performance bonuses are paid quarterly based on KPIs.
                Expense Reimbursement: Submit expense reports with receipts within 30 days.
                """
            },
            {
                "title": "IT Equipment Policy",
                "content": """
                Equipment Assignment: All employees receive a laptop, monitor, and necessary accessories.
                Security: Employees must use strong passwords and enable 2FA on all accounts.
                Personal Use: Limited personal use of company equipment is permitted.
                Maintenance: Report IT issues immediately through the helpdesk system.
                Return Policy: All equipment must be returned upon termination of employment.
                """
            },
            {
                "title": "Training and Development",
                "content": """
                Onboarding: New employees complete a 2-week onboarding program.
                Skills Training: Annual training budget of $2000 per employee for professional development.
                Certifications: Company supports industry-relevant certifications with 80% reimbursement.
                Internal Training: Monthly technical sessions and quarterly soft skills workshops.
                Career Development: Annual performance reviews include career planning discussions.
                """
            }
        ]
        
        for policy in policies:
            documents.append(Document(
                page_content=f"Policy: {policy['title']}\n\n{policy['content']}",
                metadata={"type": "policy", "title": policy['title']}
            ))
        
        return documents
    
    def _setup_qa_chains(self):
        """Setup QA chains for different contexts"""
        llm = OpenAI(temperature=0.7, openai_api_key=self.openai_api_key)
        
        # Employee QA Chain
        if self.employee_vectorstore:
            employee_prompt = PromptTemplate(
                template="""You are an AI assistant for employees of an IT company. Use the following context to answer employee questions about HR policies, payroll, colleagues, equipment, and company procedures.

Context: {context}

Question: {question}

Provide a helpful, accurate answer based on the context. If you can't find specific information, say so and suggest who they should contact for more details.

Answer:""",
                input_variables=["context", "question"]
            )
            
            self.employee_qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.employee_vectorstore.as_retriever(search_kwargs={"k": 5}),
                chain_type_kwargs={"prompt": employee_prompt}
            )
        
        # Customer QA Chain
        if self.customer_vectorstore:
            customer_prompt = PromptTemplate(
                template="""You are an AI customer service assistant for an IT company. Use the following context to help customers with their orders, invoices, project status, and general inquiries.

Context: {context}

Question: {question}

Provide a helpful, professional response. If the issue requires human intervention, explain how to escalate to a human agent.

Answer:""",
                input_variables=["context", "question"]
            )
            
            self.customer_qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.customer_vectorstore.as_retriever(search_kwargs={"k": 5}),
                chain_type_kwargs={"prompt": customer_prompt}
            )
        
        # Policy QA Chain
        if self.policy_vectorstore:
            policy_prompt = PromptTemplate(
                template="""You are an AI assistant that helps explain company policies and procedures. Use the following context to answer questions about company policies, procedures, and best practices.

Context: {context}

Question: {question}

Provide a clear, comprehensive answer based on the company policies. Include relevant details and procedures.

Answer:""",
                input_variables=["context", "question"]
            )
            
            self.policy_qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.policy_vectorstore.as_retriever(search_kwargs={"k": 5}),
                chain_type_kwargs={"prompt": policy_prompt}
            )
    
    def process_employee_query(self, question: str, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Process employee-related queries"""
        try:
            # Check if it's a policy question
            policy_keywords = ['leave', 'policy', 'payroll', 'salary', 'training', 'equipment', 'procedure']
            if any(keyword in question.lower() for keyword in policy_keywords) and self.policy_qa_chain:
                response = self.policy_qa_chain.run(question)
                return {
                    "response": response,
                    "type": "policy",
                    "escalate": False,
                    "suggestions": self._get_employee_suggestions(question)
                }
            
            # Use employee QA chain for other queries
            if self.employee_qa_chain:
                response = self.employee_qa_chain.run(question)
                return {
                    "response": response,
                    "type": "employee",
                    "escalate": False,
                    "suggestions": self._get_employee_suggestions(question)
                }
            else:
                return {
                    "response": "I'm sorry, but I don't have access to employee data at the moment. Please contact HR directly.",
                    "type": "fallback",
                    "escalate": True,
                    "suggestions": ["Contact HR", "Check employee portal"]
                }
                
        except Exception as e:
            return {
                "response": "I encountered an error processing your request. Please try again or contact support.",
                "type": "error",
                "escalate": True,
                "error": str(e)
            }
    
    def process_customer_query(self, question: str, customer_id: Optional[int] = None) -> Dict[str, Any]:
        """Process customer-related queries"""
        try:
            # Check if escalation is needed
            escalation_keywords = ['complaint', 'urgent', 'manager', 'dispute', 'refund', 'cancel']
            needs_escalation = any(keyword in question.lower() for keyword in escalation_keywords)
            
            if self.customer_qa_chain:
                response = self.customer_qa_chain.run(question)
                
                return {
                    "response": response,
                    "type": "customer",
                    "escalate": needs_escalation,
                    "suggestions": self._get_customer_suggestions(question)
                }
            else:
                return {
                    "response": "I'm sorry, but I don't have access to customer data at the moment. Please contact our support team.",
                    "type": "fallback",
                    "escalate": True,
                    "suggestions": ["Contact Support", "Check order status", "View invoices"]
                }
                
        except Exception as e:
            return {
                "response": "I encountered an error processing your request. Please try again or contact support.",
                "type": "error",
                "escalate": True,
                "error": str(e)
            }
    
    def _get_employee_suggestions(self, question: str) -> List[str]:
        """Get contextual suggestions for employee queries"""
        suggestions = []
        question_lower = question.lower()
        
        if 'leave' in question_lower:
            suggestions.extend(["Apply for leave", "Check leave balance", "View leave policy"])
        if 'payroll' in question_lower or 'salary' in question_lower:
            suggestions.extend(["View payslip", "Tax information", "Benefits overview"])
        if 'equipment' in question_lower or 'laptop' in question_lower:
            suggestions.extend(["Report IT issue", "Request equipment", "IT policies"])
        if 'training' in question_lower:
            suggestions.extend(["Browse courses", "Request training", "Certification programs"])
        
        if not suggestions:
            suggestions = ["HR Portal", "Employee Handbook", "Contact HR"]
        
        return suggestions[:4]  # Limit to 4 suggestions
    
    def _get_customer_suggestions(self, question: str) -> List[str]:
        """Get contextual suggestions for customer queries"""
        suggestions = []
        question_lower = question.lower()
        
        if 'order' in question_lower:
            suggestions.extend(["Track order", "Order history", "Modify order"])
        if 'invoice' in question_lower or 'bill' in question_lower:
            suggestions.extend(["View invoices", "Payment methods", "Download receipt"])
        if 'project' in question_lower:
            suggestions.extend(["Project status", "Timeline", "Contact project manager"])
        if 'support' in question_lower or 'help' in question_lower:
            suggestions.extend(["FAQ", "Contact support", "Live chat"])
        
        if not suggestions:
            suggestions = ["Account overview", "Order history", "Contact support", "FAQ"]
        
        return suggestions[:4]  # Limit to 4 suggestions
    
    def auto_fill_form_data(self, form_type: str, user_id: int) -> Dict[str, Any]:
        """Auto-fill form data for employees"""
        try:
            user = User.objects.get(id=user_id)
            
            # Base data that's always available
            base_data = {
                "employee_name": user.get_full_name(),
                "email": user.email,
                "username": user.username,
            }
            
            # Try to get employee data if available
            if Employee:
                try:
                    employee = Employee.objects.get(user=user)
                    base_data.update({
                        "employee_id": employee.employee_id,
                        "department": employee.department.name if employee.department else "",
                        "phone": employee.phone,
                        "manager": employee.department.manager.get_full_name() if employee.department and employee.department.manager else ""
                    })
                except Employee.DoesNotExist:
                    base_data.update({
                        "employee_id": f"EMP{user.id:04d}",
                        "department": "IT Department",
                        "phone": "",
                        "manager": ""
                    })
            else:
                # Fallback data when Employee model is not available
                base_data.update({
                    "employee_id": f"EMP{user.id:04d}",
                    "department": "IT Department", 
                    "phone": "",
                    "manager": ""
                })
            
            if form_type == "leave_request":
                return {
                    **base_data,
                    "available_leave_days": 21,  # This would come from actual leave balance
                    "form_fields": ["leave_type", "start_date", "end_date", "reason"]
                }
            elif form_type == "expense_report":
                return {
                    **base_data,
                    "form_fields": ["expense_date", "category", "amount", "description", "receipt"]
                }
            
            return base_data
            
        except Exception as e:
            return {"error": f"Could not retrieve employee data: {str(e)}"}
    
    def get_personalized_recommendations(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get personalized recommendations for customers"""
        try:
            # This would typically analyze past orders, preferences, etc.
            # For now, returning sample recommendations
            return [
                {
                    "type": "service",
                    "title": "Cloud Migration Service",
                    "description": "Based on your recent inquiries about scalability",
                    "confidence": 0.85
                },
                {
                    "type": "product",
                    "title": "Enterprise Security Package",
                    "description": "Recommended for companies of your size",
                    "confidence": 0.72
                }
            ]
        except Exception as e:
            return []


# Global chatbot instance
chatbot_service = None

def get_chatbot_service():
    """Get or create chatbot service instance"""
    global chatbot_service
    if chatbot_service is None:
        chatbot_service = SmartChatbotService()
    return chatbot_service
