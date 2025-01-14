# Introdução


###  **CRIAÇÃO DO WS**


1. Inicializar o ROS:

`source /opt/ros/foxy/setup.bash`

`. install/setup.bash`

2. Criar pasta do workspace

`mkdir -p ~/ros2_ws/src`
  

O comando `-p` é utilizado para criar a pasta e a subpasta

  
3. Comando `build`

é como se fosse a inicialização do pacote, sempre que houver alguma atualização em algum dos arquivos precisa utilizar o comando. Sempre que executado, esse comando cria as pastas build, install e log.

`colcon build`

**CRIAÇÃO DO PACOTE**

Posso escolher entre utilizar python ou c++. cmake ou ament python

Comandos para python e c++

	ros2 pkg create --build-type ament_python <package_name>

	ros2 pkg create isi_ros2_example –build-type ament_python –dependencies rclpy –node-name classic_pub
	



INICIALIZAÇÃO DO AMBIENTE DO PACOTE
`source install/setup.bash`

https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html

#### Parâmetros

É um valor de configuração de um node. Integer, floats, booleans e lists.


Comandos gerais

`rqt `

é um pacote para gerenciamento de informações do ROS 

`ros2 node list` É útil para verificarmos os nodes ativos, posso interagir com eles. 

## LAB 1

Crie um pacote chamado `lab1_pkg` que de suporte para código em c e em python. Declare a dependência em `ackermann_msgs`. 


O node utiliza o pacote ROS chamado `ackerman_msgs`, que precisa ser importado no inicio do código. Ele disponibiliza um tipo especifico de informação, normalmente é utilizado tipo float, string e integer. Nesse caso utilizamos o tipo `AckermannDriveStamped`, na declaração do tópico de publicação. 

Além da mensagem ser desse tipo especifico, é preciso declarar os parâmetros solicitados (v e d). O trecho do código com essas informações esta apresentado a seguir. 

``` 
class Talker(Node):

	def __init__(self):
		super().__init__('Talker')

		# Declarar parâmetros
		self.declare_parameter('v', 1.0) # velocidade
		self.declare_parameter('d', 1.0) # ângulo de direção

		self.publisher_ = self.create_publisher(AckermannDriveStamped, 
		'drive', 10)

		self.timer = self.create_timer(0.1, self.publish_message)
```

A última linha é um temporizador para publicar a mensagem a cada 0.1 segundo. Em resumo, essa parte inicial declara a classe Talker, que é o nome do node, com os parâmetros e tópico de publicação com o tipo de mensagem publicada e o nome do tópico, em conjunto com um temporizador para repetir a mensagem publicada. 

No segundo trecho do código efetuamos a coleta dos valores dos parâmetros, declaramos a estrutura da mensagem como `AckermannDriveStamped()`. Nesse ponto declaramos que a estrutura `msg.drive.atributo` recebe o parâmetro especifico desejado. Estruturada a mensagem, a parte final é um comando para publicar a mensagem e registrar o que foi publicado no log. 

```
	def publish_message(self):

		v = self.get_parameter('v').get_parameter_value().double_value
		d = self.get_parameter('d').get_parameter_value().double_value

		# Criar a mensagem
		msg = AckermannDriveStamped()
		msg.drive.speed = v
		msg.drive.steering_angle = d


		# Publicar a mensagem
		self.publisher_.publish(msg)
		self.get_logger().info(f'Publishing: speed={v}, steering_angle={d}')

```


Resumo do que preciso fazer: 
1 - dar o source na pasta do workspace 
2 - rodar o pacote com ros2 run lab1_pkg talker

#### Launch file

É preciso adicionar linha de código do launch no arquivo setup.py do pacote, pra que o ROS reconheça que existem arquivos de launch. Também é preciso tomar cuidado com o nome dos arquivos na pasta install da sua workspace, o executável que o launch busca é o que está na pasta install. 

`(os.path.join('share', package_name, "launch"), glob('launch/*')), #pegando todos os arquivos de launch.`

o launch utilizado 

```
<launch>
	<node pkg="lab1_pkg" exec="talker" name="Talker" output="screen" />
	<node pkg="lab1_pkg" exec="listener" name="Relay"
output="screen" />

  

</launch>
```
_________________


comandos: 

`ros2 run lab1_pkg talker`
`ros2 run lab1_pkg listener `


nome do pacote: lab1_pkg 
executável (nome do arquivo python): talker
name (nome do nó, nome da classe): 

ros2 launch <package_name> <launch_file_name>
