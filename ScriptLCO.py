from selenium import  webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import datetime
import time


## Interaccion con la web mediante webdriver

listaRfc = ["Aqui se añaden los RFC a buscar"]

PATH = "/home/kevin/Documentos/ValeTotalScript/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://cssoft.mx/")

rfcConError = []
listaRfcExpiracion = []  

diaActual = datetime.datetime.now()

print("RFC con error:")


for i in listaRfc:
    busquedaRFC = driver.find_element_by_name("rfc").send_keys(i,Keys.RETURN)
    busquedaFecha = driver.find_elements_by_xpath("//table/tbody/tr/td[3]")
    fechas = [i.text for i in busquedaFecha] 
    diccionarioRfcfecha = {i:fechas}
    longitudRfcDias = (len(*diccionarioRfcfecha.values()))
    ## Verifica si la lista esta vacia, si lo esta lo agrega a rfcConError
    
    contador = 0

    for k,v in diccionarioRfcfecha.items():
        if not v:
            print("Error:",k)
            rfcConError.append(k)
        ## Verifica si este rfc no ha expirado
        for j in v:
            nuevoFormato  = datetime.datetime.strptime(j ,'%Y-%m-%d %H:%M:%S')
            diferencia = (nuevoFormato - diaActual).days
            if diferencia < 0:
                contador = contador + 1
        if (longitudRfcDias - contador) == 0:
            if len(v) == 0:
                pass
            else:
                print("Expiracion:",k)
                listaRfcExpiracion.append(k)
    # Da click en boton para volver a ingresar un RFC
    boton = driver.find_element_by_xpath("//div[@class='col text-center mt-5']/a[@class='btn btn-primary']").click()

driver.quit() 

print("Total de RFC con error:" , len(rfcConError))
print(rfcConError)

print("Total de RFC expirados:", len(listaRfcExpiracion))
print(listaRfcExpiracion)
## Creacion de CSV de los RFC con error
df = pd.DataFrame(rfcConError,columns=['RFCerror'])
df.to_csv( 'RFCerror' + archivo +'.csv',index=False)

