# -*- coding: utf-8 -*-
'''
Created on 10.05.2013

@author: nimrod
'''
from translation.common import vcard_fields, merge_buzzwords, merge_chunk_buzzwords, \
        categories_buzz, subcategories_buzz, OrderedDict
import translation.english as english

mandatory_fields = set(vcard_fields) - set(['fax-mobile', 'email2', 'email3', 'facebook', 'google', 'twitter',
                        'skype', 'credit-cards', 'intl-area-code', 'comment'])


categories = dict(see='veja', do='faça', buy='compre', eat='come', drink='beba',
                   sleep='durma', listing='outro')

vcard_items = dict(type='tipo', name='nome', alt='alt',
                   address=u'endereço', directions=u'direções', phone='tel', email='email',
                   fax='fax', url='site', hours='funcionamento', price=u'preço',
                   checkin='checkin', checkout='checkout', lat='lat', long='long',
                   description='sobre')

abbreviations = 'av ed pred r rod est estr tr pç jd st pq jl th tel nr no'.split()

def translate_vcard(vcard):
    ret = OrderedDict((vcard_items.get(k, k), vcard.get(k, ''))
                      for k in english.vcard_fields if k in mandatory_fields or vcard.get(k))
    del ret['subtype']
    ret['tipo'] = categories.get(ret.get('tipo'), ret.get('tipo'))
    if ret['tipo'] != 'durma':
        for i in ('checkin', 'checkout'):
            if not ret.get(i) and i in ret:
                del ret[i]
    ret['tag'] = vcard['type'].lower()
    return ret

def format_vcard(vcard):
    vcard_type = vcard.pop('tipo', 'outro')
    return u'{{%s |%s}}' % (vcard_type, ' |'.join(u"%s=%s" % (key, val) for key, val in vcard.iteritems()))

buzzwords = dict(
    sleep=dict(
               general=set(['quarto', 'pousada', 'ar condicionado',
                         'banheira', 'café da manhã', 'limpo',
                         'lavanderia', 'veranda', 'janela', 'malas', 'cabo',
                         'cama', 'ventilador', 'geladeira', 'banheiro', 'sala',
                         'acomodar', 'tenente', 'preço', 'acomodação',
                         'cheiro', 'faxineira', 'pessoal', 'serviço']),
                hotel=set([ 'segura', 'frigobar', 'seguro', 'privado', 'estrela', 'sauna',
                        'residência', 'balneário', 'buffet', 'academia',
                        'suite', 'reserva', 'exclusivo', 'elegante']),
                hostel=set(['albergue'])),

    eat=dict(
             general=set(['restaurante', 'comer', 'come', 'comida', 'cozinha', 'gastronomia',
                          'prato', 'café da manhã', 'vinho', 'culinária', 'massa', 'refeição',
                          'sopa', 'ovo', 'vegetariano', 'vegetariana', 'bife', 'carne', 'frango',
                          'porco', 'churrasco', 'picanha', 'feijoada', 'feijão', 'porção', 'porções',
                          'salada', 'rodízio', 'pizza', 'quilo', 'kilo', 'self-service', 'grill',
                          'sobremesa', 'petisco', 'petiscos', 'calabresa', 'linguiça', 'caldo',
                          'caldos', 'fruta', 'almoço', 'jantar', 'especialidades', 'panqueca',
                          'tapioca', 'assado', 'frita', 'frito', 'assada', 'brasa', 'chapa']),
             fastfood=set(['hambúrguer', 'búrguer', 'cachorro quente', 'lanche', 'salgado',
                           'salgados', 'coxinha', 'misto quente', 'sanduíche', 'lancheteria']),
             indian=set(['indiano', 'indiana', 'karê', 'carê']),
             seafood=set(['frutos do mar', 'mariscos', 'peixe', 'carangueijo', 'siri', 'atum',
                          'salmão', 'camarão', 'langosta', 'pescado', 'dourado', 'bacalhão']),
             asian=set(['asiático', 'asiática', 'carê', 'karê', 'vietnamito', 'vietnamita',
                        'japonês', 'japonesa', 'chinês', 'chinesa', 'tailandês', 'tailandesa',
                        'filipino', 'filipina', 'yakisoba', 'sushi', 'rolinho primavera', 'sashimi']),
             italiano=set(['massa', 'pizza', 'italiano', 'italiana', 'bolonês', 'bolonesa', 'lasanha']),
             german=set(['alemão', 'alemã', 'baviera']),
             french=set(['francês', 'francesa', 'vinho']),
             mexican=set(['mexicano'])),
    drink=dict(
              cafe=set(['café', 'bebida', 'chá', 'sorvete', 'suco', 'iogurte', 'yogurte', 'ovo']),
              bar=set(['bar', 'bebida', 'cerveja', 'chope', 'chopp', 'música', 'ao vivo', 'galera',
                       'público'', ''cervejaria'', ''chopperia', 'choperia', 'snooker', 'tarde',
                       'madrugada', 'noite', 'pátio', 'guitarra', 'violão', 'choro', 'bossa nova',
                       'rock', 'eletrônica', 'banda', 'mulher', 'garota', 'dardos', 'esportes']),
              nightclub=set(['boate', 'clube', 'discoteca', 'coctel', 'cocteis', 'vinho', 'música',
                             'dançar', 'balada', 'ar livre'])),
    see=dict(
             general=set(['museu', 'biblioteca', 'coleção']),
             art=set(['arte', 'galeria', 'pintura', 'escultura', 'óleo', 'estátua', 'madeira',
                      'contemporário', 'contemporária']),
             nature=set(['parque', 'jardim', 'verde', 'caminho', 'caminhar', 'floresta', 'bosque',
                         'lago', 'lagoa', 'lagoinha', 'praia', 'natura', 'vista', 'parque nacional',
                         'parque estadual', 'chafariz', 'fonte', 'gruta', 'caverna', 'cachoeira',
                         'foz', 'cascata', 'serra', 'montanha', 'morro', 'vale', 'paisagem',
                         'árvore']),
             historical=set(['palácio', 'guerra', 'passeio', 'prefeitura', 'monumento', 'torre',
                             'imperador', 'rei', 'rainha', 'príncipe', 'castelo', 'forte',
                             'fortaleza', 'dinâstia', 'epoca', 'década', 'século', 'antigo',
                             'estrutura', 'prédio', 'edifício', 'construido', 'construida',
                             'inaugurado', 'inaugurada', 'governo', 'sede', 'reformado',
                             'reformada', 'neoclássico', 'neoclássica', 'gótico', 'gótica',
                             'presidente', 'residência', 'casarão', 'assentamento', 'parede',
                             'ruína', 'ruínas', 'liberdade', 'bandeirantes', 'inconfidência',
                             'república', 'democracia', 'país', 'oficial', 'independência',
                             'ocupação'])),
    buy=dict(
             general=set(['comprar', 'compras', 'compra', 'barato', 'caro', 'loja', 'mercado',
                          'feira', 'item', 'bens', 'mercadoria', 'varejo', 'preço', 'economizar',
                          'regatear', 'dinheiro', 'desconto', 'vender', 'vendas', 'comercial']),
             cloth=set(['roupa', 'camisa', 'vestido', 'acessórios', 'chapeu', 'sapato', 'couro',
                        'terno', 'gravata', 'poliéster', 'lã', 'algodão', 'cinta']),
             books=set(['papel', 'livro', 'revista', 'jornal', 'jornais', 'impressa', 'literatura',
                        'português']),
             touristy=set(['lembrança', 'relógio', 'joalheria', 'presente', 'exótico', 'especialidade'])),
    do=dict(
            general=set(['guia', 'criança', 'evento', 'piscina']),
            outdoor=set(['mergulhar', 'mergulho', 'caminhar', 'trilho', 'bicicleta', 'ciclismo',
                         'pescar', 'pescaria', 'pesqueiro', 'nadar', 'asa delta', 'boia-cross',
                         'cavalo', 'vela', 'surfe', 'surfar', 'passeio']),
            indoor=set(['filme', 'tela', 'show', 'concerto', 'peça', 'teatro', 'festa', 'festival',
                        'zoológico']),
            learn=set(['aprender', 'universidade', 'curso', 'aulo', 'ensinar', 'estudante', 'aluno',
                       'idioma', 'língua']))
)


chunk_buzzwords = dict(
    address=set(['avenida', 'ave', 'av', 'prédio', 'edifício', 'ed', 'boulevarde', 'rodovia', 'rod', 'via',
                 'trav.', 'travéssia', 'praça', 'pr.', 'bairro', 'b', 'estrada', 'est.', 'distrito', 'zona',
                 'z.', 's/n']),
    directions=set(['cruzamento', 'interseção', 'esquina', 'esq.', 'frente', 'atrás', 'ao lado', 'do lado',
                    'perto', 'próximo', 'dentro', 'esquero', 'esquera', 'direita', 'direito', 'ônibus', 'parada',
                    'metro', 'estação', 'metrô', 'bonde']),
    alt=set(['conhecido', 'conhecida', 'também', 'antigo']),
    phone=set(['fone', 'número', 'no']),
    hours=set(['horários', 'horas', 'funcionamento', 'de', 'á', 'diário', '2a', '3a', '4a', '5a', '6a', 'sab',
               'dom', 'sábado', 'domingo', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'semana', '24',
               'h', 'fev', 'abr', 'mai', 'maio', 'ago', 'set', 'dez', 'meia noite', 'meio dia', 'tarde']),
    fax=set(['número']),
    price=set(['R$', 'preço', 'real', 'reais', 'dólar', 'dólares', 'libra', 'moeda', 'a partir de',
               'ienes', 'ien', 'rublo'])
)

buzzwords = merge_buzzwords(buzzwords, english.buzzwords)
categories_dict = categories_buzz(buzzwords)
subcategories_dict = subcategories_buzz(buzzwords)

chunk_buzzwords = merge_chunk_buzzwords(chunk_buzzwords, english.chunk_buzzwords)
