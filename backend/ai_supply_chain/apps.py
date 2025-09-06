"""
AI Supply Chain Django App Configuration
"""

from django.apps import AppConfig


class AiSupplyChainConfig(AppConfig):
    """Configuration for AI Supply Chain app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_supply_chain'
    verbose_name = 'AI Supply Chain Optimization'
    
    def ready(self):
        """Initialize app when Django starts"""
        # Import signals here to avoid circular imports
        # We can add signal handlers for automatic AI processing
        pass
