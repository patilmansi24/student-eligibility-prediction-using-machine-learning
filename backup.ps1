$DATE = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$BACKUP_FILE = "supabase_backup_$DATE.sql"

pg_dump `
  --dbname="postgresql://postgres.pftiuwlednjrgibgqteq:Owskar%405125@aws-1-ap-south-1.pooler.supabase.com:5432/postgres?sslmode=require" `
  --format=plain `
  --no-owner `
  --no-privileges `
  --verbose `
  --file="$BACKUP_FILE"

Write-Output "✅ Backup completed: $BACKUP_FILE"
