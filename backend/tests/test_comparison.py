from backend.agents.compliance.agent import ComplianceAgent

agent = ComplianceAgent()
result = agent.analyze("scripts/output/pdfs/spec_1.pdf", "scripts/output/pdfs/vendor_submittal_1.pdf")

print(result)
