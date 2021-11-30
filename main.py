from typing import List
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Path
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

#--------------------------------------

class BaseProdutoModel(BaseModel):
    codigo: int
    descricao: str
    preco: float
    
class AdicionarProdutoModel(BaseProdutoModel):
    codigo: int

class AlterarProdutoModel(BaseProdutoModel):
    pass
    

produtos = []

@app.post('/produtos', status_code=status.HTTP_201_CREATED)
def adicionar_produtos(produto: AdicionarProdutoModel):
    produtos.append(produto)
   
@app.get('/produtos')
def lista_produtos():
    return produtos


@app.put('/produtos/{codigo}')
def alterar_produto(codigo: int, produto:AlterarProdutoModel):
    retorno = list(filter(lambda a:a.codigo == codigo, produtos))
    print("produtos",retorno)
    if not retorno:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                detail = f'Produto com código:{codigo} não encontrado')
    
    produto_encontrado = retorno[0]
    print("produto_encontrado",produto_encontrado)
    produto_encontrado.descricao = produto.descricao
    produto_encontrado.preco = produto.preco
    
    return produto_encontrado

@app.patch('/produtos/alterar/{codigo}') # ver com o professor
def alterar_produto(codigo:int, novo_preco:float, float = Body(...)):
    retorno = list(filter(lambda a:a.codigo == codigo,produtos))
    if not retorno:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                detail = f'Produto com código:{codigo} não encontrado')
        
    produto_encontrado = retorno[0]
    produto_encontrado.preco = novo_preco

    return produto_encontrado

@app.delete('/produtos/{codigo}', status_code=status.HTTP_204_NO_CONTENT)
def remover_produtos(codigo: int):
    retorno = list(filter(lambda a: a[1].codigo == codigo, enumerate(produtos)))
    if not retorno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'Produto com código:{codigo} não encontrado')

    i, _ = retorno[0]
    del produtos[i]



    
#--------------------------------------

class BaseCategoriaModel(BaseModel):
    tipo: str
    publico_alvo: str
    rentabilidade: float
        

categorias = []

@app.post('/categoria', status_code=status.HTTP_201_CREATED)
def adicionar_categorias(categoria: BaseCategoriaModel):
    categorias.append(categoria)

@app.get('/categoria}')
def lista_categorias():
    return categorias

@app.put('/categoria/{tipo}')
def altera_categoria(tipo: str, categoria: BaseCategoriaModel):
    resultado = list(filter(lambda c: c.tipo == tipo, categorias))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Categoria tipo {tipo} não foi encontrada.')

    categoria_encontrada = resultado[0]
    categoria_encontrada.tipo = categoria.tipo
    categoria_encontrada.publico_alvo = categoria.publico_alvo
    categoria_encontrada.rentabilidade = categoria.rentabilidade

    return categoria_encontrada


@app.patch('/categoria/altera-rentabilidade/{tipo}')
def altera_rentabilidade(tipo: str, nova_rentabilidade: float = Body(...)):
    resultado = list(filter(lambda c: c.tipo == tipo, categorias))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Categoria tipo {tipo} não foi encontrada.')
    
    categoria_encontrada = resultado[0]
    categoria_encontrada.rentabilidade = nova_rentabilidade

    return categoria_encontrada

#--------------------------------------    

class BaseFornecedorModel(BaseModel):
    empresa: str
    cnpj: str
    tipo_contrato: str


fornecedores = []

@app.post('/fornecedor', status_code=status.HTTP_201_CREATED)
def adicionar_fornecedor(fornecedor:BaseFornecedorModel):
    fornecedores.append(fornecedor)

@app.get('/fornecedores')
def lista_forncedores():
    return fornecedores

@app.put('/fornecedores/{cnpj}')
def alterar_fornecedor(cnpj:str, fornecedor:BaseFornecedorModel):
    retorno = list(filter(lambda a:a.cnpj == cnpj, fornecedores))
    if not retorno:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                detail = f'Produto com cnpj:{cnpj} não encontrado')
    
    fornecedor_encontrado = retorno[0]
    fornecedor_encontrado.empresa = fornecedor.empresa
    fornecedor_encontrado.cnpj = fornecedor.cnpj
    fornecedor_encontrado.tipo_contrato = fornecedor.tipo_contrato
    
    return fornecedor_encontrado

@app.patch('/fornecedores/alterar/{cnpj}') # ver com o professor
def alterar_produto(cnpj:int, novo_contrato:str  = Body(...)):
    retorno = list(filter(lambda a:a.cnpj == cnpj,produtos))
    if not retorno:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                detail = f'O fornecedor com o :{cnpj} não encontrado')
        
    fornecedor_encontrado = retorno[0]
    fornecedor_encontrado.tipo_contrato = novo_contrato

    return fornecedor_encontrado

@app.delete('/fornecedores/{cnpj}', status_code=status.HTTP_204_NO_CONTENT)
def remover_fornecedores(cnpj: int):
    retorno = list(filter(lambda a: a[1].cnpj == cnpj, enumerate(fornecedores)))
    if not retorno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'O fornecedor com o :{cnpj} não encontrado')

    i, _ = retorno[0]
    del fornecedores[i]
#--------------------------------------

class BaseCompradorModel(BaseModel):
    identificador: int
    comprador_nome: str
    genero: str
    faixa_etaria: str
    nacionalidade: str

compradores = []

@app.post('/comprador', status_code=status.HTTP_201_CREATED)
def adicionar_comprador(comprador: BaseCompradorModel):
    compradores.append(comprador)

@app.get('/compradores')
def lista_compradores():
    return compradores


@app.delete('/delete/{identificador}', status_code=status.HTTP_204_NO_CONTENT)
def remover_comprador(identificador: int):
    resultado = list(filter(lambda c: c[1].identificador == identificador, enumerate(compradores)))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Comprador com o nome {comprador_nome} não foi encontrado')
    i, _ = resultado[0]
    del compradores[i]

@app.put('/compradores/{identificador}')
def altera_comprador(identificador: str, comprador: BaseCompradorModel = Body(...)):
    resultado = list(filter(lambda c: c.identificador == identificador, compradores))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Comprador com o identificador {identificador} não foi encontrado.')

    comprador_encontrado = resultado[0]
    comprador_encontrado.identificador = comprador.identificador
    comprador_encontrado.comprador_nome = comprador.comprador_nome
    comprador_encontrado.genero = comprador.genero
    comprador_encontrado.faixa_etaria = comprador.faixa_etaria
    comprador_encontrado.nacionalidade = comprador.nacionalidade

    return comprador_encontrado

    