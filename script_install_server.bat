if exist C:\SYS_AUTO2\python27\python.exe (
	if exist c:\SYS_AUTO2\Server\meter_access_server\server.py (
	cd c:\SYS_AUTO2\Server\meter_access_server
		c:\SYS_AUTO2\python27\python.exe server.py
	 ) else (
		mkdir C:\SYS_AUTO2\Server
		CD C:\SYS_AUTO2\Server
			git clone --single-branch --branch master https://gitlab-solutions.rmm.scom/g361355/meter_access_server.git
			CD C:\SYS_AUTO2\Server\meter_access_server\
			c:\SYS_AUTO2\python27\python.exe server.py
		 )
		) else (
  mkdir C:\SYS_AUTO2
  CD C:\SYS_AUTO2\
  mkdir python27
  cd python27
  git clone https://gitlab-solutions.rmm.scom/g361355/outils.git
	if exist c:\SYS_AUTO2\Server\meter_access_server\server.py (
		CD c:\SYS_AUTO2\Server\meter_access_server\
		c:\SYS_AUTO2\python27\outils\outils\Python27\python.exe server.py
	) else (
		mkdir C:\SYS_AUTO2\Server\
		cd C:\SYS_AUTO2\Server\
		git clone --single-branch --branch master https://gitlab-solutions.rmm.scom/g361355/meter_access_server.git
		CD C:\SYS_AUTO2\Server\meter_access_server\
		c:\SYS_AUTO2\python27\outils\outils\Python27\python.exe server.py
		)
)