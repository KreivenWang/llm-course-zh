Write-Host "激活虚拟环境并运行疫情数据分析脚本..." -ForegroundColor Green
Write-Host ""

# 激活虚拟环境
& .\venv\Scripts\Activate.ps1

# 运行数据分析脚本
python calculate_confirmed_cases.py

Write-Host ""
Write-Host "脚本执行完成。" -ForegroundColor Green