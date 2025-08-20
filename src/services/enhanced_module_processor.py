#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Enhanced Module Processor
Processador avançado para geração dos 16 módulos de análise
"""

import os
import logging
import json
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class EnhancedModuleProcessor:
    """Processador para geração de todos os módulos de análise"""

    def __init__(self):
        """Inicializa o processador"""
        self.modules_list = [
            'anti_objecao',
            'avatars',
            'concorrencia',
            'drivers_mentais',
            'funil_vendas',
            'insights_mercado',
            'palavras_chave',
            'plano_acao',
            'posicionamento',
            'pre_pitch',
            'predicoes_futuro',
            'provas_visuais',
            'metricas_conversao',
            'estrategia_preco',
            'canais_aquisicao',
            'cronograma_lancamento'
        ]

        self.prompts = self._initialize_prompts()
        logger.info(f"✅ Enhanced Module Processor inicializado com {len(self.modules_list)} módulos")

    def _initialize_prompts(self) -> Dict[str, str]:
        """Inicializa os prompts específicos para cada módulo"""
        return {
            'anti_objecao': """
            Analise os dados coletados e crie um sistema completo de tratamento de objeções para este produto/serviço.

            ESTRUTURA OBRIGATÓRIA:

            # Sistema Anti-Objeção Avançado

            ## 1. Objeções Identificadas
            [Liste as 10 principais objeções baseadas nos dados reais coletados]

            ## 2. Estratégias de Tratamento
            [Para cada objeção, forneça estratégias específicas de tratamento]

            ## 3. Scripts de Resposta
            [Scripts prontos para usar em vendas]

            ## 4. Provas e Evidências
            [Dados concretos para rebater objeções]

            Baseie-se integralmente nos dados reais fornecidos. Seja específico e prático.
            """,

            'avatars': """
            Com base nos dados coletados, crie avatares detalhados do público-alvo ideal para este produto/serviço.

            ESTRUTURA OBRIGATÓRIA:

            # Avatares do Público-Alvo

            ## Avatar Principal
            [Descrição completa baseada nos dados reais]

            ## Avatares Secundários
            [2-3 avatares alternativos]

            ## Características Comportamentais
            [Padrões de comportamento identificados nos dados]

            ## Dores e Necessidades
            [Baseado nos insights coletados]

            ## Canais de Comunicação Preferidos
            [Onde encontrar esses avatares]

            Use apenas informações extraídas dos dados reais fornecidos.
            """,

            'concorrencia': """
            Analise a concorrência identificada nos dados coletados e crie um mapeamento estratégico completo.

            ESTRUTURA OBRIGATÓRIA:

            # Análise Competitiva Detalhada

            ## 1. Mapeamento de Concorrentes
            [Lista dos principais concorrentes identificados]

            ## 2. Análise SWOT Comparativa
            [Forças, fraquezas, oportunidades e ameaças]

            ## 3. Estratégias de Diferenciação
            [Como se posicionar de forma única]

            ## 4. Monitoramento Contínuo
            [Métricas e indicadores para acompanhar]

            Baseie toda análise nos dados reais coletados sobre a concorrência.
            """,

            'drivers_mentais': """
            Identifique e analise os drivers mentais presentes no público-alvo baseado nos dados coletados.

            ESTRUTURA OBRIGATÓRIA:

            # Drivers Mentais Identificados

            ## 1. Drivers Primários
            [Os 5 principais drivers identificados nos dados]

            ## 2. Drivers Secundários
            [Drivers de apoio e complementares]

            ## 3. Aplicação Prática
            [Como usar cada driver em marketing e vendas]

            ## 4. Mensagens Persuasivas
            [Exemplos práticos baseados nos drivers]

            Utilize apenas insights extraídos dos dados reais fornecidos.
            """,

            'funil_vendas': """
            Projete um funil de vendas otimizado baseado nos dados coletados e características do público-alvo.

            ESTRUTURA OBRIGATÓRIA:

            # Funil de Vendas Estratégico

            ## 1. Etapas do Funil
            [Consciência, Interesse, Consideração, Intenção, Compra, Retenção]

            ## 2. Conteúdo por Etapa
            [Tipos de conteúdo para cada fase]

            ## 3. Métricas de Conversão
            [KPIs esperados baseados nos dados do mercado]

            ## 4. Pontos de Otimização
            [Onde melhorar baseado na análise]

            Baseie todas as recomendações nos dados reais coletados.
            """,

            'insights_mercado': """
            Compile insights estratégicos de mercado baseados em todos os dados coletados.

            ESTRUTURA OBRIGATÓRIA:

            # Insights Estratégicos de Mercado

            ## 1. Tendências Identificadas
            [Tendências emergentes no setor]

            ## 2. Oportunidades de Mercado
            [Gaps e oportunidades identificadas]

            ## 3. Ameaças e Desafios
            [Riscos e obstáculos identificados]

            ## 4. Recomendações Estratégicas
            [Ações específicas baseadas nos insights]

            Use exclusivamente dados reais coletados para gerar insights.
            """,

            'palavras_chave': """
            Analise os dados coletados e identifique as palavras-chave mais relevantes para o negócio.

            ESTRUTURA OBRIGATÓRIA:

            # Estratégia de Palavras-Chave

            ## 1. Palavras-Chave Primárias
            [Top 10 palavras identificadas nos dados]

            ## 2. Palavras-Chave de Cauda Longa
            [Termos específicos e nichos]

            ## 3. Análise de Volume e Competição
            [Baseado nos dados coletados]

            ## 4. Estratégia de Conteúdo
            [Como usar as palavras-chave]

            Extraia palavras-chave diretamente dos dados reais fornecidos.
            """,

            'plano_acao': """
            Crie um plano de ação executável baseado em todas as análises realizadas.

            ESTRUTURA OBRIGATÓRIA:

            # Plano de Ação Estratégico

            ## 1. Objetivos Principais
            [Metas claras baseadas nos dados]

            ## 2. Ações Prioritárias (30 dias)
            [Primeiros passos críticos]

            ## 3. Ações de Médio Prazo (90 dias)
            [Desenvolvimento e implementação]

            ## 4. Ações de Longo Prazo (1 ano)
            [Consolidação e expansão]

            ## 5. Recursos Necessários
            [Time, tecnologia, orçamento]

            Baseie todo o plano nos insights extraídos dos dados reais.
            """,

            'posicionamento': """
            Desenvolva uma estratégia de posicionamento baseada nos dados coletados sobre mercado e concorrência.

            ESTRUTURA OBRIGATÓRIA:

            # Estratégia de Posicionamento

            ## 1. Análise de Posicionamento Atual
            [Como o mercado percebe produtos similares]

            ## 2. Proposta de Posicionamento
            [Posição única baseada nos dados]

            ## 3. Diferenciação Competitiva
            [O que torna este produto único]

            ## 4. Mensagem Principal
            [Comunicação clara do posicionamento]

            ## 5. Validação de Mercado
            [Como testar o posicionamento]

            Use apenas insights dos dados reais coletados.
            """,

            'pre_pitch': """
            Desenvolva uma estrutura de pré-pitch baseada nos dados comportamentais coletados.

            ESTRUTURA OBRIGATÓRIA:

            # Estrutura de Pré-Pitch

            ## 1. Abertura Impactante
            [Hook baseado nas dores identificadas]

            ## 2. Identificação do Problema
            [Problemas reais do público-alvo]

            ## 3. Agravamento da Dor
            [Consequências de não resolver]

            ## 4. Apresentação da Solução
            [Como o produto resolve especificamente]

            ## 5. Prova Social
            [Evidências e validação]

            ## 6. Call to Action
            [Próximo passo claro]

            Baseie toda estrutura nos dados reais sobre o público-alvo.
            """,

            'predicoes_futuro': """
            Analise tendências nos dados coletados e faça predições fundamentadas sobre o futuro do mercado.

            ESTRUTURA OBRIGATÓRIA:

            # Predições de Mercado

            ## 1. Tendências Emergentes
            [Padrões identificados nos dados]

            ## 2. Predições de Curto Prazo (6 meses)
            [Mudanças esperadas]

            ## 3. Predições de Médio Prazo (2 anos)
            [Evolução do mercado]

            ## 4. Predições de Longo Prazo (5 anos)
            [Transformações estruturais]

            ## 5. Implicações Estratégicas
            [Como se preparar para o futuro]

            Base todas as predições em dados e tendências reais identificadas.
            """,

            'provas_visuais': """
            Identifique e organize provas visuais baseadas nos dados coletados sobre sucesso no mercado.

            ESTRUTURA OBRIGATÓRIA:

            # Sistema de Provas Visuais

            ## 1. Tipos de Prova Social
            [Depoimentos, cases, números]

            ## 2. Fontes de Credibilidade
            [Onde encontrar provas confiáveis]

            ## 3. Estratégia de Apresentação
            [Como usar as provas efetivamente]

            ## 4. Cronograma de Coleta
            [Como obter mais provas]

            Base as recomendações nos exemplos reais encontrados nos dados.
            """,

            'metricas_conversao': """
            Defina métricas de conversão baseadas nos dados de mercado coletados.

            ESTRUTURA OBRIGATÓRIA:

            # Sistema de Métricas de Conversão

            ## 1. KPIs Principais
            [Métricas críticas baseadas no negócio]

            ## 2. Benchmarks de Mercado
            [Padrões identificados nos dados]

            ## 3. Metas Realistas
            [Objetivos baseados em dados reais]

            ## 4. Ferramentas de Medição
            [Como acompanhar as métricas]

            Use dados reais coletados para estabelecer benchmarks.
            """,

            'estrategia_preco': """
            Desenvolva uma estratégia de precificação baseada na análise de mercado realizada.

            ESTRUTURA OBRIGATÓRIA:

            # Estratégia de Precificação

            ## 1. Análise de Preços da Concorrência
            [Dados coletados sobre pricing]

            ## 2. Percepção de Valor
            [Como o mercado valoriza soluções similares]

            ## 3. Estratégias de Preço
            [Diferentes abordagens de pricing]

            ## 4. Testes Recomendados
            [Como validar a estratégia]

            Baseie toda estratégia nos dados reais de mercado coletados.
            """,

            'canais_aquisicao': """
            Identifique os melhores canais de aquisição baseados no comportamento do público-alvo nos dados.

            ESTRUTURA OBRIGATÓRIA:

            # Canais de Aquisição Otimizados

            ## 1. Canais Identificados
            [Onde o público-alvo está presente]

            ## 2. Priorização de Canais
            [Ordem de implementação baseada em dados]

            ## 3. Estratégia por Canal
            [Abordagem específica para cada um]

            ## 4. Orçamento Sugerido
            [Distribuição de investimento]

            Use apenas canais validados pelos dados comportamentais coletados.
            """,

            'cronograma_lancamento': """
            Crie um cronograma de lançamento baseado nas melhores práticas identificadas nos dados de mercado.

            ESTRUTURA OBRIGATÓRIA:

            # Cronograma de Lançamento

            ## 1. Fase de Preparação
            [Atividades pré-lançamento]

            ## 2. Fase de Soft Launch
            [Teste com público restrito]

            ## 3. Fase de Lançamento Oficial
            [Go-to-market completo]

            ## 4. Fase de Otimização
            [Ajustes pós-lançamento]

            ## 5. Marcos e Deadlines
            [Cronograma detalhado]

            Baseie o timeline em dados reais sobre lançamentos similares no mercado.
            """
        }

    async def generate_all_modules(self, session_id: str) -> Dict[str, Any]:
        """
        Gera todos os 16 módulos de análise

        Args:
            session_id: ID da sessão para carregar dados

        Returns:
            Dict com resultados da geração dos módulos
        """
        logger.info(f"🚀 Iniciando geração de todos os módulos para sessão: {session_id}")

        try:
            # 1. Carrega dados necessários
            relatorio_coleta = self._load_relatorio_coleta(session_id)
            resumo_sintese = self._load_resumo_sintese(session_id)

            if not relatorio_coleta or not resumo_sintese:
                raise Exception("Dados base não encontrados para geração dos módulos")

            # 2. Prepara contexto principal
            main_context = self._prepare_main_context(relatorio_coleta, resumo_sintese)

            # 3. Gera cada módulo
            results = {
                'session_id': session_id,
                'timestamp': datetime.now().isoformat(),
                'total_modules': len(self.modules_list),
                'successful_modules': 0,
                'failed_modules': 0,
                'modules': {},
                'errors': []
            }

            # Importa ai_manager
            from services.ai_manager import ai_manager

            for module_name in self.modules_list:
                try:
                    logger.info(f"📝 Gerando módulo: {module_name}")

                    # Obtém prompt específico do módulo
                    module_prompt = self.prompts.get(module_name, self._get_default_prompt(module_name))

                    # Combina prompt com contexto
                    full_prompt = f"{module_prompt}\n\n=== DADOS PARA ANÁLISE ===\n{main_context}"

                    # Gera conteúdo usando IA com ferramentas se necessário
                    if module_name in ['concorrencia', 'predicoes_futuro', 'insights_mercado']:
                        # Módulos que podem se beneficiar de busca adicional
                        module_content = await ai_manager.generate_with_tools(
                            full_prompt,
                            context="",
                            tools=['google_search'],
                            max_iterations=3
                        )
                    else:
                        # Módulos baseados apenas nos dados coletados
                        module_content = await ai_manager.generate_text(full_prompt, max_tokens=4096)

                    # Salva módulo
                    self._save_module(session_id, module_name, module_content)

                    results['modules'][module_name] = {
                        'status': 'success',
                        'length': len(module_content),
                        'generated_at': datetime.now().isoformat()
                    }
                    results['successful_modules'] += 1

                    logger.info(f"✅ Módulo {module_name} gerado com sucesso ({len(module_content)} caracteres)")

                except Exception as e:
                    error_msg = f"Erro ao gerar módulo {module_name}: {str(e)}"
                    logger.error(f"❌ {error_msg}")

                    results['modules'][module_name] = {
                        'status': 'error',
                        'error': str(e),
                        'generated_at': datetime.now().isoformat()
                    }
                    results['failed_modules'] += 1
                    results['errors'].append(error_msg)

            # 4. Gera relatório consolidado
            await self._generate_consolidated_report(session_id, results)

            logger.info(f"✅ Geração concluída: {results['successful_modules']}/{results['total_modules']} módulos")
            return results

        except Exception as e:
            logger.error(f"❌ Erro na geração dos módulos: {e}")
            raise

    def process_all_modules_from_massive_data(
        self, 
        massive_data: Dict[str, Any], 
        context: Dict[str, Any], 
        session_id: str
    ) -> Dict[str, Any]:
        """Processa módulos a partir dos dados massivos coletados"""
        
        try:
            # Executa geração normal de módulos
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    self.generate_all_modules(session_id)
                )
            finally:
                loop.close()
            
            # Adiciona informações dos dados massivos
            result['massive_data_summary'] = {
                'total_sources': massive_data.get('statistics', {}).get('total_sources', 0),
                'collection_time': massive_data.get('statistics', {}).get('collection_time', 0),
                'screenshot_count': massive_data.get('statistics', {}).get('screenshot_count', 0)
            }
            
            result['processing_summary'] = {
                'successful_modules': result.get('successful_modules', 0),
                'total_modules_processed': result.get('total_modules', 0),
                'processing_timestamp': datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro no processamento de módulos: {e}")
            return {
                'success': False,
                'error': str(e),
                'processing_summary': {
                    'successful_modules': 0,
                    'total_modules_processed': 0,
                    'processing_timestamp': datetime.now().isoformat()
                }
            }

    def _load_relatorio_coleta(self, session_id: str) -> Optional[str]:
        """Carrega relatório de coleta da sessão"""
        try:
            file_path = f"analyses_data/{session_id}/relatorio_coleta.md"
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            return None
        except Exception as e:
            logger.error(f"❌ Erro ao carregar relatório de coleta: {e}")
            return None

    def _load_resumo_sintese(self, session_id: str) -> Optional[Dict]:
        """Carrega resumo de síntese da sessão"""
        try:
            file_path = f"analyses_data/{session_id}/resumo_sintese.json"
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"❌ Erro ao carregar resumo de síntese: {e}")
            return None

    def _prepare_main_context(self, relatorio_coleta: str, resumo_sintese: Dict) -> str:
        """Prepara contexto principal para os módulos"""
        context = f"""
RELATÓRIO DE COLETA DE DADOS:
{relatorio_coleta}

RESUMO DE SÍNTESE (JSON):
{json.dumps(resumo_sintese, indent=2, ensure_ascii=False)}

INSTRUÇÕES IMPORTANTES:
- Use APENAS os dados fornecidos acima
- Seja específico e baseado em evidências reais
- Evite generalizações sem base nos dados
- Forneça insights práticos e executáveis
- Mantenha o foco no mercado e público-alvo identificados
"""
        return context

    def _get_default_prompt(self, module_name: str) -> str:
        """Retorna prompt padrão para módulos não especificados"""
        return f"""
        Analise os dados fornecidos e crie um relatório detalhado sobre {module_name.replace('_', ' ')}.

        ESTRUTURA OBRIGATÓRIA:
        # {module_name.replace('_', ' ').title()}

        ## Análise dos Dados
        [Análise baseada nos dados reais fornecidos]

        ## Insights Principais
        [Principais descobertas]

        ## Recomendações Práticas
        [Ações específicas baseadas na análise]

        ## Conclusões
        [Síntese dos pontos principais]

        Use exclusivamente os dados fornecidos para sua análise.
        """

    def _save_module(self, session_id: str, module_name: str, content: str):
        """Salva módulo gerado"""
        try:
            modules_dir = f"analyses_data/{session_id}/modules"
            os.makedirs(modules_dir, exist_ok=True)

            file_path = f"{modules_dir}/{module_name}.md"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.debug(f"💾 Módulo {module_name} salvo em {file_path}")

        except Exception as e:
            logger.error(f"❌ Erro ao salvar módulo {module_name}: {e}")
            raise

    async def _generate_consolidated_report(self, session_id: str, results: Dict):
        """Gera relatório consolidado de todos os módulos"""
        try:
            logger.info("📋 Gerando relatório consolidado final...")

            # Carrega todos os módulos gerados
            modules_content = {}
            modules_dir = f"analyses_data/{session_id}/modules"

            for module_name in self.modules_list:
                if results['modules'].get(module_name, {}).get('status') == 'success':
                    file_path = f"{modules_dir}/{module_name}.md"
                    if os.path.exists(file_path):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            modules_content[module_name] = f.read()

            # Gera relatório final consolidado
            consolidated_report = self._build_consolidated_report(session_id, results, modules_content)

            # Salva relatório final
            final_report_path = f"analyses_data/{session_id}/relatorio_final_completo.md"
            with open(final_report_path, 'w', encoding='utf-8') as f:
                f.write(consolidated_report)

            logger.info(f"✅ Relatório consolidado salvo em: {final_report_path}")

        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório consolidado: {e}")

    def _build_consolidated_report(self, session_id: str, results: Dict, modules_content: Dict) -> str:
        """Constrói o relatório consolidado final"""
        report = f"# RELATÓRIO FINAL CONSOLIDADO - ARQV30 Enhanced v3.0\n\n"
        report += f"**Sessão:** {session_id}  \n"
        report += f"**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}  \n"
        report += f"**Módulos Gerados:** {results['successful_modules']}/{results['total_modules']}\n\n"

        report += "---\n\n"

        report += "## SUMÁRIO EXECUTIVO\n\n"
        report += "Este relatório consolidado apresenta a análise ultra-detalhada realizada pelo sistema ARQV30 Enhanced v3.0, contemplando {len(self.modules_list)} módulos especializados de análise estratégica.\n\n"

        report += "### Módulos Incluídos:\n"
        for i, module_name in enumerate(self.modules_list, 1):
            status = results['modules'].get(module_name, {}).get('status', 'not_generated')
            status_icon = "✅" if status == 'success' else "❌"
            module_title = module_name.replace('_', ' ').title()
            report += f"{i}. {status_icon} {module_title}\n"

        report += "\n---\n\n"

        for module_name in self.modules_list:
            if module_name in modules_content:
                module_title = module_name.replace('_', ' ').title()
                report += f"## {module_title}\n\n"
                report += modules_content[module_name]
                report += "\n\n---\n\n"

        report += f"""
## INFORMAÇÕES TÉCNICAS

**Sistema:** ARQV30 Enhanced v3.0  
**Sessão:** {session_id}  
**Data de Geração:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}  
**Módulos Processados:** {results['successful_modules']}/{results['total_modules']}  
**Status:** {'Completo' if results['failed_modules'] == 0 else 'Parcial'}

### Estatísticas de Geração:
- ✅ Sucessos: {results['successful_modules']}
- ❌ Falhas: {results['failed_modules']}
- 📊 Taxa de Sucesso: {(results['successful_modules']/results['total_modules']*100):.1f}%

---

*Relatório gerado automaticamente pelo ARQV30 Enhanced v3.0*
"""

        return report

    def get_module_status(self, session_id: str) -> Dict[str, Any]:
        """Retorna status dos módulos gerados"""
        try:
            modules_dir = f"analyses_data/{session_id}/modules"

            status = {
                'session_id': session_id,
                'total_modules': len(self.modules_list),
                'generated_modules': 0,
                'modules': {}
            }

            for module_name in self.modules_list:
                file_path = f"{modules_dir}/{module_name}.md"
                if os.path.exists(file_path):
                    stat = os.stat(file_path)
                    status['modules'][module_name] = {
                        'exists': True,
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    }
                    status['generated_modules'] += 1
                else:
                    status['modules'][module_name] = {
                        'exists': False,
                        'size': 0,
                        'modified': None
                    }

            return status

        except Exception as e:
            logger.error(f"❌ Erro ao verificar status dos módulos: {e}")
            return {'error': str(e)}

# Instância global
enhanced_module_processor = EnhancedModuleProcessor()