# -*- coding: utf-8 -*-
'''
Created on 10.05.2013

@author: nimrod
'''
from collections import OrderedDict
from translation.common import vcard_fields, merge_buzzwords, categories_buzz, subcategories_buzz
import translation.english as english

mandatory_fields = set(vcard_fields) - set(['fax-mobile', 'email2', 'email3', 'facebook', 'google', 'twitter',
                        'skype', 'credit-cards', 'checkin', 'checkout', 'alt', 'email', 'fax', 'lat', 'long',
                        'intl-area-code', 'mobile', 'comment'])


categories = dict(see='veja', do='faça', buy='compre', eat='coma', drink='beba',
                   sleep='durma', listing='item')

vcard_items = dict(type='tipo', name='nome', alt='alt',
                   address='endereço', directions='direções', phone='tel', email='email',
                   fax='fax', url='site', hours='funcionamento', price='preço',
                   checkin='checkin', checkout='checkout', lat='lat', long='long',
                   description='sobre')

abbreviations = 'av ed pred r rod est estr tr pç jd st pq jl th tel nr no'

def translate_vcard(vcard):
    ret = OrderedDict((vcard_items.get(k, k), vcard.get(k, ''))
                      for k in english.vcard_fields)
    for k in ret.keys():
        if not ret[k] and k not in mandatory_fields:
            del ret[k]
    del ret['subtype']
    ret['tipo'] = categories.get(ret.get('tipo'), ret.get('tipo'))
    ret['tag'] = vcard['type'].lower()
    return ret

buzzwords = dict(
    sleep=dict(
               general={'quarto', 'pousada', 'ar condicionado',
                         'banheira', 'café da manhã', 'limpo',
                         'lavanderia', 'veranda', 'janela', 'malas', 'cabo',
                         'cama', 'ventilador', 'geladeira', 'banheiro', 'sala',
                         'acomodar', 'tenente', 'preço', 'acomodação',
                         'cheiro', 'faxineira', 'pessoal', 'serviço'},
                hotel={ 'segura', 'frigobar', 'seguro', 'privado', 'estrela', 'sauna',
                        'residência', 'balneário', 'buffet', 'academia',
                        'suite', 'reserva', 'exclusivo', 'elegante'},
                hostel={'albergue'})
)

buzzwords = merge_buzzwords(buzzwords, english.buzzwords)
categories_dict = categories_buzz(buzzwords)
subcategories_dict = subcategories_buzz(buzzwords)

