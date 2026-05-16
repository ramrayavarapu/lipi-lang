#!/usr/bin/env python3
"""
Manual smoke test to verify agentic_integration imports work correctly.
This repository-root script is intended for local debugging and is not
automatically exercised by CI unless it is explicitly wired into a workflow.
"""

import sys
import os

# Add src to path (same as demo file)
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("Testing agentic_integration import...")
    from agentic_integration import AdaptiveAIEngineeringGovernanceSystem
    print("✅ AdaptiveAIEngineeringGovernanceSystem imported successfully")
    
    print("Testing system initialization...")
    system = AdaptiveAIEngineeringGovernanceSystem()
    print("✅ System initialized successfully")
    
    print("Testing dashboard generation...")
    dashboard = system.generate_enterprise_dashboard()
    print("✅ Dashboard generated successfully")
    print(f"   System Status: {dashboard['system_status']}")
    
    print("\n🎉 All imports and basic operations working correctly!")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("\nTrying to diagnose missing dependencies...")
    
    # Test individual imports
    try:
        from agentic_governance import AgenticGovernanceOrchestrator, AgentSelectionContext, AgentType
        print("✅ agentic_governance imports work")
    except ImportError as e:
        print(f"❌ agentic_governance import failed: {e}")
    
    try:
        from agentic_intelligence_extended import CostAwarenessEngine, ReliabilityFramework
        print("✅ agentic_intelligence_extended imports work")
    except ImportError as e:
        print(f"❌ agentic_intelligence_extended import failed: {e}")
    
    sys.exit(1)

except Exception as e:
    print(f"❌ Runtime Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)