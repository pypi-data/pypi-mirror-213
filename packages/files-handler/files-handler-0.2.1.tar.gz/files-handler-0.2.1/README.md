## Instalação da biblioteca

- Para instalar a biblioteca basta chamar no console "pip install files-handler"

## Inicialização da biblioteca

- Para iniciar a biblioteca, basta importar as duas classes, ou apenas a de interesse com o "from files_handler import s3_handler, folders_handler"
- O próximo passo é instanciar a classe respectiva:

  s3_handler_class = s3_handler(bucket, path_ref)
  Para essa classe é preciso passar no construtor, o bucket do S3 e também um diretorio de referência local para obter e salvar os arquivos

  folders_handler_class = folders_handler(path_ref)
  Para essa classe é preciso passar no construtor o diretório de referência que contém as pastas a serem manipuladas.

- Após isso, é só chamar as funções de cada classe, um exemplo:
  folders_handler_class.verify_and_create_folder('input')
  Dessa forma, a função verifica a pasta no diretório 'path_ref + input', e caso não exista, ela será criada

## Descrição das classes da biblioteca

A biblioteca possui duas classes, uma para lidar com a conexão com o S3 e outra para lidar com o gerenciamento das pastas para as análises

O s3_handler possui três metódos, sendo eles:

- get_image_from_s3_bucket
  Responsável por obter uma imagem do S3

- upload_image_to_s3_bucket
  Responsável por upar a imagem resultando no S3

- check_if_file_already_exists
  Verificar se já existe algum arquivo ou imagem no S3

O folders_handler possui dois métodos, sendo eles:

- clear_folder
  Responsável por limpar a pasta que foi passada como parâmetro

- verify_and_create_folder
  - Responsável por verificar se a pasta já existe, se não, ele cria a pasta que foi passada como parâmetro

## Testar a biblioteca

Para testar a biblioteca é preciso instalar os pacotes do requirements.txt, configurar as variáveis de ambiente no tests/s3_handler_tests.py e rodar os comandos na raiz da biblioteca:

python -m unittest tests/s3_handler_tests.py
python -m unittest tests/folders_handler_tests.py

## Subir uma nova versão da biblioteca

Para subir uma nova versão da biblioteca no Pypi é preciso ter uma conta no [PyPi](https://pypi.org/), ter instalado o [twine](https://pypi.org/project/twine/) na máquina, modificar o número da versão na linha 18 do setup.py, e rodar os seguintes comandos na raiz da biblioteca:

python setup.py sdist bdist_wheel
python -m twine upload dist/\* --verbose --skip-existing

A URL da lib no PyPi é essa: https://pypi.org/project/files-handler/
