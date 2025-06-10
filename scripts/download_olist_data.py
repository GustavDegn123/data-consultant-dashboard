import kagglehub

# Henter datasættet og gemmer i cache-mappe
path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")

print("✅ Datasættet er hentet til:", path)
