@echo off
echo 激活虚拟环境并运行疫情数据分析脚本...
echo.

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 运行数据分析脚本
python calculate_confirmed_cases.py

echo.
echo 脚本执行完成。
pause