import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/fixedrace', methods=['POST'])
def evaluatefixedrace():
    s = request.data.decode()
    names = ['Francisco Finchum', 'Joseph Jarosz', 'Lyman Laseter', 'Irvin Insley', 'Corine Cottrill', 'Spring Sawin', 'Charita Collett', 'Justa Jeffery', 'Marcellus Mallow', 'Rossana Rackers', 'Fabian Fogel', 'Annamarie Ahern', 'Zada Zynda', 'Darren Dudley', 'Chester Caldwell', 'Marco Mena', 'Douglas Delima', 'Jared Jinkins', 'Craig Christoff', 'Monroe Middlebrook', 'Shelli Scheuerman', 'Olive Osgood', 'Napoleon Negrete', 'Brady Borda', 'Gaston Glotfelty', 'Arlinda Alarcon', 'Sharyl Shepler', 'Vida Veal', 'Emily Eckles', 'Florine Faison', 'Enriqueta Ealy', 'Arron Ammerman', 'Renea Rausch', 'Josh Jensen', 'Fletcher Felty', 'Adaline Anwar', 'Felice Forte', 'Amos Alward', 'Fairy Faria', 'Dominic Dolce', 'Milford Mcqueen', 'Casey Collinsworth', 'Olympia Oliphant', 'Dalia Degen', 'Pamula Parrinello', 'Jenniffer Jen', 'Kali Krupp', 'Judith Juntunen', 'Livia Luse', 'Kaycee Klem', 'Willian Wahlen', 'Caitlyn Croskey', 'Vanda Vonderheide', 'Dorathy Detweiler', 'Tomas Tilman', 'Huey Haberkorn', 'Shirly Sosebee', 'Adina Able', 'Gary Ginsburg', 'Sacha Stanforth', 'Olinda Oakley', 'Carlo Chute', 'Elbert Ehrman', 'Chase Colone', 'Cecila Cribb', 'Lucas Lucht', 'Colin Crail', 'Alfonso Allred', 'Alysia Auslander', 'Sixta Sulton', 'Farrah Frasure', 'Brice Benigno', 'Leana Lynde', 'Demetrius Dixion', 'Margit Mello', 'Trinity Trueblood', 'Emmett Estepp', 'Reed Rotolo', 'Cora Carruth', 'Lola Leyendecker', 'Anibal Abler', 'Nenita Nunnery', 'Terry Tietz', 'Autumn Acuff', 'Alanna Ayoub', 'Jesse Julio', 'Clemencia Carcamo', 'Alex Appleton', 'Jewel Jaeger', 'Boris Batts', 'Yu Yeates', 'Damien Degraff', 'Thanh Tammaro']
    order = {name: i for i, name in enumerate(names)}
    s = s.split(',')
    s = [name.strip() for name in s]
    inside = list()
    outside = list()
    for name in s:
        if name in order.keys():
            inside.append(name)
        else:
            outside.append(name)
    inside.sort(key = lambda name: order[name])
    for name in outside:
        inside.append(name)
    return ', '.join(inside)