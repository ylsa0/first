from suds import sudsobject
from suds.client import Client

if __name__ == '__main__':
    url = 'http://172.16.183.6/szhtkjwsORA/ZwxminfoService65.asmx?wsdl'
    client = Client(url)
    #print(client)
    result = client.service.GetZgInfo('11142020034')
    print(sudsobject.asdict(result)['ZgInfo'][0]['Ygmc'])
