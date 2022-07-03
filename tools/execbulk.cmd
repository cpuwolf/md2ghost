call env.cmd

::pip install pyjwt
::pip install pytz


@for /R "D:\works\GitHub\discuzX2hexo\blog\source\_posts\" %%f in (*.md) do (
	python.exe postghost.py "%%f"
)

popd
pause