from psi_cloud import PSIClient

client = PSIClient(api_key="psi_live_XXXXXXXXXXXXXXXX")

try:
    resultado = client.check_sufficiency(n=8, bits=2.9)

    if resultado["deterministic_achieved"]:
        print("✅ Sistema resoluble:", resultado["recommendation"])
    else:
        print("⚠️ Sistema insuficiente:", resultado["recommendation"])

    print(f"Créditos restantes: {resultado['credits_remaining']}")

except Exception as e:
    print(f"Error: {e}")
    
    
    
    
    
    
    
    
    