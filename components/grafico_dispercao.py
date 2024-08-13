import pandas as pd
import plotly.express as plot
import  pandas as pd
from dados.grafico_repository import RepositoryGrafico


class GraficoDispersao:
    
    def __init__(self) -> None:
        self.repository_banco = RepositoryGrafico()


    def constroi_grafico_dispersao_brasil(self, modalidade=1, indice_min=0, indice_max=100, peso_p1=1, peso_p2=1):
        
        indice_brasil = self.repository_banco.dados_todos_estados(modalidade=modalidade,
                                                            indice_min=indice_min, 
                                                            indice_max=indice_max,
                                                            peso_p1=peso_p1, 
                                                            peso_p2=peso_p2
                                                        )
        indice_brasil = pd.DataFrame(indice_brasil)

        fig = plot.scatter(
            indice_brasil, 
            x="indice", 
            y="area_km2", 
            size="indice", 
            color="região",
            hover_name="nome", 
            log_x=True, 
            size_max=60
        )

        fig.update_layout(
            xaxis_title="Índice de Conformidade",
            yaxis_title="Área em KM2",
            paper_bgcolor='rgba(0,0,0,0)', 
        )
        return fig

