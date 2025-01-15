'''
Função que calcula os valores dos coeficientes k`s

l0: comprimento do link 0
l1: comprimento do link 1
l2: comprimento do link 2
l3: comprimento do link 3
teta: angulo de entrada

'''


#Função que calcula os valores dos K's (k1,k2 e k3)
def sol_ks(l0,l1,l2,l3,tet):
  k1 = -2*l1*l3*np.sin(tet)
  k2 = 2*l3*(l0-(l1*np.cos(tet)))
  k3 = l0**2 + l1**2 -l2**2 + l3**2 - 2*l0*l1*np.cos(tet)
  return k1,k2,k3

#Função que calcula o angulo dependente
def sol_phi(k1,k2,k3):
  delta = k1**2 + k2**2 - k3**2

  #expressão quadratica
  pos = k1 + np.sqrt(delta)
  neg = k1 - np.sqrt(delta)

  # raizes da expressão quadratica. Pode ser um sistema com raizes imaginarias
  phi1 = 2 * np.arctan2(k3-k2,pos) + np.pi
  phi2 = 2 * np.arctan2(k3-k2,neg) + np.pi
  return phi1


'''
Função que calcula um dos angulos dependentes

phis: angulos dependentes
tetas: angulos de entrada

'''

def solve_phis(l0,l1,l2,l3,tetas):
  try:
    count = 0
    phis = np.zeros(len(tetas))
    for i in tetas:
      #chamar as funções para cada valor de pi
      k1,k2,k3 = sol_ks(l0,l1,l2,l3,i)
      phi = sol_phi(k1,k2,k3)
      phis[count] = phi
      count +=1
      #end
  except:
      k1,k2,k3 = sol_ks(l0,l1,l2,l3,tetas)
      phi = sol_phi(k1,k2,k3)
      phis = phi

  return phis

'''
Função que calcula um dos angulos dependentes

alphas: angulos dependentes
tetas: angulos de entrada

'''

def sol_alpha(l0,l1,l2,l3,teta,phi):
  try:
    count = 0
    alphas = np.zeros(len(teta))

    for i in range(len(teta)):
      x = l0 - l1*np.cos(teta[count]) + l3*np.cos(phi[count])
      y = - l1*np.sin(teta[count]) + l3*np.sin(phi[count])

      alpha = np.arctan2(y , x)

      alphas[count] = alpha
      count +=1

  except:

    x = l0 - l1*np.cos(teta) + l3*np.cos(phi)
    y = - l1*np.sin(teta) + l3*np.sin(phi)

    alpha = np.arctan2(y , x)

    alphas = alpha

  return alphas

'''
Função que calcula as velocidades angulares alpha e phi
a partir da velocidade angular de entrada


'''

def sol_velocidades(l1, l2, l3, teta, alpha, phi, v_teta):
  # Inicializa as velocidades
  try:
    v_alphas = np.zeros(len(teta))
    v_phis = np.zeros(len(teta))

    for count in range(len(teta)):
    # Monta a matriz
      A = np.array([[l2 * np.sin(alpha[count]), -l3 * np.sin(phi[count])],
                  [-l2 * np.cos(alpha[count]), l3 * np.cos(phi[count])]])

    # Vetor do lado direito da equação
      B = np.array([-l1 * np.sin(teta[count]) * v_teta,
                    l1 * np.cos(teta[count]) * v_teta])

    # Resolve o sistema para encontrar dot_alpha e dot_phi
      v_alpha, v_phi = np.linalg.solve(A, B)

      v_alphas[count] = v_alpha
      v_phis[count] = v_phi
  except:
    A = np.array([[l2 * np.sin(alpha), -l3 * np.sin(phi)],
                  [-l2 * np.cos(alpha), l3 * np.cos(phi)]])

    # Vetor do lado direito da equação
    B = np.array([-l1 * np.sin(teta) * v_teta,
                    l1 * np.cos(teta) * v_teta])

    # Resolve o sistema para encontrar dot_alpha e dot_phi
    v_alpha, v_phi = np.linalg.solve(A, B)

    v_alphas = v_alpha
    v_phis = v_phi


  return v_alphas, v_phis


def graficos_pos(tetas_deg,phis_deg,alphas_deg):
  plt.plot(tetas_deg,phis_deg)
  plt.xlabel("θ")
  plt.ylabel("φ(θ)")
  plt.show()

  print("\n")
  plt.plot(tetas_deg,alphas_deg)
  plt.xlabel("θ")
  plt.ylabel("α(θ)")
  plt.show()

def graficos_vel(tetas_deg,alphas_dot,phis_dot):
  plt.plot(tetas_deg, alphas_dot, label='Velocidade Alpha (rad/s)')
  plt.xlabel("θ")
  plt.ylabel("dα/dt (θ,t)")
  plt.legend()
  plt.show()
  print("\n")

  plt.plot(tetas_deg, phis_dot, label='Velocidade Phi (rad/s)')
  plt.xlabel("θ")
  plt.ylabel("dφ/dt (θ,t)")
  plt.legend()
  plt.show()


def graficos_pos2(tetas_deg, phis_deg, alphas_deg, theta_target_deg):
    # Encontre o índice do valor mais próximo de theta_target_deg
    idx = (np.abs(tetas_deg - theta_target_deg)).argmin()

    # Gráfico de θ versus φ
    plt.plot(tetas_deg, phis_deg, label='φ(θ)')
    plt.scatter(tetas_deg[idx], phis_deg[idx], color='red')  # Marca o ponto de interesse
    plt.text(tetas_deg[idx], phis_deg[idx], f'θ={theta_target_deg:.1f}°, φ={phis_deg[idx]:.2f}°',
             fontsize=12, color='red', ha='right')
    plt.xlabel("θ (graus)")
    plt.ylabel("φ(θ) (graus)")
    plt.legend()
    plt.show()

    # Gráfico de θ versus α
    plt.plot(tetas_deg, alphas_deg, label='α(θ)')
    plt.scatter(tetas_deg[idx], alphas_deg[idx], color='blue')  # Marca o ponto de interesse
    plt.text(tetas_deg[idx], alphas_deg[idx], f'θ={theta_target_deg:.1f}°, α={alphas_deg[idx]:.2f}°',
             fontsize=12, color='blue', ha='right')
    plt.xlabel("θ (graus)")
    plt.ylabel("α(θ) (graus)")
    plt.legend()
    plt.show()



def main():
  #(inicio, final, n divisoes), cria uma lista de angulos de entrada usada para calcular os outros angulos
  tetas = np.linspace(0 , (2*np.pi), 100)

  #calcula os outros angulos em função de θ
  phis = solve_phis(80,20,66,56,tetas)
  alphas = sol_alpha(80,20,66,56,tetas,phis)

  tetas_deg = np.rad2deg(tetas)
  phis_deg = np.rad2deg(phis)
  alphas_deg = np.rad2deg(alphas)

  #Velocidade de entrada na coordenada generalizada θ
  v_teta = 25.0 #rad/s

  # Calcula as velocidades angulares
  alphas_dot, phis_dot = sol_velocidades(20,66,56, tetas, alphas, phis, v_teta)

  # Plot das funções
  #print("Graficos de posição: \n")
  #graficos_pos2(tetas_deg,phis_deg,alphas_deg)

  print("Graficos de posição: \n")
  theta_target_deg = 60  # O valor de θ para marcar no gráfico
  graficos_pos2(tetas_deg, phis_deg, alphas_deg, theta_target_deg)

  print("\n Graficos de velocidade: \n")
  graficos_vel(tetas_deg,alphas_dot,phis_dot)

  return alphas_dot, phis_dot






