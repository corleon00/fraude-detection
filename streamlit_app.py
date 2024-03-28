import base64
import streamlit as st
import pandas as pd
import joblib


def main():
    # Charger l'image depuis votre PC
    image_path = 'C:/Users/alaba/OneDrive/Bureau/ModelDeployment/image.jpg'
    
    # Convertir l'image en base64
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    # Définir une image de fond pour l'application en utilisant du code CSS
    def set_background(image_path):
        bin_str = get_base64_of_bin_file(image_path)
        page_bg_img = '''
        <style>
        body {
            background-image: url("data:image/jpeg;base64,%s");
            background-size: cover;
        }
        </style>
        ''' % bin_str
        st.markdown(page_bg_img, unsafe_allow_html=True)

    # Appeler la fonction pour définir l'image en arrière-plan
    set_background(image_path)

# Titre de l'application
st.title('Détection de Fraude')

# Liste des options de la catégorie
categories = ['','misc_net', 'gas_transport', 'food_dining', 'shopping_pos',
              'grocery_pos', 'kids_pets', 'personal_care', 'shopping_net',
              'entertainment', 'health_fitness', 'home', 'misc_pos', 'travel',
              'grocery_net']

# Liste des genres
genders = ['M', 'F']

# Liste des emplois
job_options = [
       'Entrer l\'emploi','Clothing/textile technologist', 'Biochemist, clinical',
       'Journalist, newspaper', 'Sports administrator',
       'Scientific laboratory technician', 'Librarian, public',
       'Scientist, biomedical', 'Toxicologist',
       'Senior tax professional/tax inspector', 'Surgeon',
       'Chief of Staff', 'Therapist, occupational', 'Financial trader',
       'Product manager', 'Engineer, control and instrumentation',
       'Editor, commissioning', 'Water engineer', 'Press sub',
       'Engineer, maintenance', 'Geoscientist',
       'Civil engineer, contracting', 'Radio broadcast assistant',
       'Mining engineer', 'Clinical cytogeneticist', 'Therapist, art',
       'Engineer, petroleum', 'Research scientist (medical)',
       'Comptroller', 'Therapist, sports', 'Technical brewer',
       'Librarian, academic', 'Forensic psychologist',
       'Accounting technician', 'Television production assistant',
       'Chartered public finance accountant', 'Engineer, biomedical',
       'Oceanographer', 'Herbalist', 'Engineer, production',
       'Operations geologist', 'Probation officer', 'TEFL teacher',
       'Licensed conveyancer', 'Chief Executive Officer', 'Solicitor',
       'Immigration officer', 'Event organiser', 'Paramedic',
       "Politician's assistant", 'Occupational psychologist',
       'Nutritional therapist', 'Education officer, museum',
       'Web designer', 'Occupational hygienist', 'Dispensing optician',
       'Tourism officer', 'Land', 'Jewellery designer', 'Oncologist',
       'Video editor', 'Surveyor, minerals', 'Medical secretary',
       'Prison officer', 'Exercise physiologist',
       'Educational psychologist', 'Surveyor, land/geomatics',
       'Manufacturing systems engineer', 'Facilities manager',
       'Cabin crew', "Nurse, children's", 'Curator', 'Warden/ranger',
       'Phytotherapist', 'Programme researcher, broadcasting/film/video',
       'Chief Operating Officer', 'Art therapist', 'Gaffer',
       'Designer, ceramics/pottery', 'Geologist, engineering', 'Make',
       'Public relations account executive', 'Film/video editor',
       'Public librarian', 'Set designer', 'Economist', 'Physiotherapist',
       'Quantity surveyor', 'Engineering geologist',
       'Further education lecturer', 'Biomedical scientist',
       'Research scientist (physical sciences)',
       'Television/film/video producer', 'Immunologist',
       'Investment banker, corporate', 'Arboriculturist',
       'Health service manager', 'Accountant, chartered certified',
       'Music therapist', 'Audiological scientist', 'Theme park manager',
       'Optometrist', 'Chiropodist', 'Retail banker',
       'Communications engineer', 'Development worker, community',
       'Structural engineer', 'Counsellor', 'Health physicist',
       'Hydrologist', 'Trading standards officer',
       'Glass blower/designer', 'Archivist', 'Secretary/administrator',
       'Podiatrist', 'Sub', 'Chartered accountant',
       'Outdoor activities/education manager', 'Chief Technology Officer',
       'IT trainer', 'Production engineer', 'Buyer, industrial',
       'Land/geomatics surveyor', 'Teacher, early years/pre',
       'Financial adviser', 'Petroleum engineer',
       'Horticultural therapist', 'Museum education officer',
       'Futures trader', 'Advice worker', 'Engineer, building services',
       'Logistics and distribution manager',
       'Corporate investment banker', 'Scientist, audiological',
       'Psychologist, forensic', 'Education administrator',
       'Furniture designer', 'Medical sales representative',
       'Engineer, electronics', 'Engineer, mining',
       'Psychologist, counselling', 'Artist', 'Naval architect',
       'Trade mark attorney', 'Research scientist (life sciences)',
       'Teacher, special educational needs', 'Site engineer',
       'Chartered legal executive (England and Wales)', 'Acupuncturist',
       'Training and development officer', 'Mechanical engineer',
       'Environmental consultant', 'Building control surveyor',
       'Sport and exercise psychologist', 'Production manager',
       'Radio producer', 'Town planner', 'Chief Strategy Officer',
       'Cartographer', 'Exhibitions officer, museum/gallery',
       'Community arts worker', 'Research officer, political party',
       'Horticulturist, commercial', 'Therapist, horticultural',
       'Camera operator', 'Designer, exhibition/display',
       'Engineer, automotive',
       'Administrator, charities/voluntary organisations',
       'Seismic interpreter', 'Engineer, agricultural', 'Producer, radio',
       'Fitness centre manager', 'Chief Financial Officer',
       'Pension scheme manager', 'Investment analyst', 'Geochemist',
       'Freight forwarder', 'Energy engineer',
       'Operational investment banker', 'Legal secretary',
       'Engineer, land', 'Hospital doctor', 'Physicist, medical',
       'Magazine features editor', 'Special educational needs teacher',
       'Commercial horticulturist', 'Risk analyst', 'Systems analyst',
       'Teacher, English as a foreign language',
       'Tourist information centre manager', 'Research scientist (maths)',
       'Company secretary', 'Psychiatrist', 'Chemical engineer',
       'Engineer, drilling', 'Call centre manager',
       'Psychologist, sport and exercise', 'General practice doctor',
       'Horticultural consultant', 'Sales executive',
       'Telecommunications researcher', 'Engineer, civil (consulting)',
       'Contractor', 'Bookseller', 'Pathologist',
       'Equality and diversity officer', 'Private music teacher',
       'Scientist, physiological', 'Field trials officer',
       'Mental health nurse', 'Editor, magazine features',
       'Press photographer', 'Colour technologist', 'Analytical chemist',
       'Network engineer', 'Retail buyer', 'Scientist, research (maths)',
       'Lawyer', 'Charity officer', 'Management consultant',
       'Designer, jewellery', 'Materials engineer', 'Fine artist',
       'Museum/gallery conservator', 'Administrator',
       'Designer, furniture', 'Presenter, broadcasting',
       'Heritage manager', 'Tax inspector',
       'Engineer, broadcasting (operations)', 'Secondary school teacher',
       'Emergency planning/management officer', 'Multimedia programmer',
       'Chemist, analytical', 'Theatre director',
       'Programmer, multimedia', 'Investment banker, operational',
       'English as a second language teacher',
       'Commercial/residential surveyor', 'Doctor, hospital',
       'Human resources officer', 'Claims inspector/assessor',
       'Engineer, structural', 'Pharmacist, hospital',
       'Health promotion specialist', 'Designer, multimedia',
       'Designer, industrial/product', 'Geologist, wellsite',
       'Chartered loss adjuster',
       'Scientist, clinical (histocompatibility and immunogenetics)',
       'Archaeologist',
       'Historic buildings inspector/conservation officer', 'Osteopath',
       'Barrister', 'Physiological scientist', 'Doctor, general practice',
       'Regulatory affairs officer', 'Building surveyor',
       'Broadcast presenter', 'Optician, dispensing', 'Soil scientist',
       'Police officer', 'Pilot, airline', 'Pharmacist, community',
       'Architect', 'Teacher, secondary school',
       'Programmer, applications', 'Geneticist, molecular',
       'Scientist, marine', 'Systems developer', 'Applications developer',
       'Animal nutritionist', 'Product/process development scientist',
       'Farm manager', 'Commissioning editor', 'Copywriter, advertising',
       'Tax adviser', 'Science writer',
       'Armed forces training and education officer',
       'Careers information officer', 'Air cabin crew',
       'Public affairs consultant', 'Insurance claims handler',
       'Research officer, trade union', 'Radiographer, diagnostic',
       'Accountant, chartered public finance', 'Barista', 'Firefighter',
       'Learning mentor', 'Designer, interior/spatial',
       'Advertising copywriter', 'Paediatric nurse',
       'Lecturer, higher education', 'Transport planner',
       'Cytogeneticist', 'Pensions consultant',
       'Development worker, international aid', 'Landscape architect',
       'Surveyor, rural practice', 'Theatre manager',
       'Special effects artist', 'Television camera operator',
       'Lexicographer', 'Tree surgeon', 'Producer, television/film/video',
       'Editor, film/video', 'Energy manager',
       'Community development worker', 'Visual merchandiser',
       'Administrator, education', 'Minerals surveyor',
       'Electronics engineer', 'Musician',
       'Planning and development surveyor', 'Civil Service fast streamer',
       'Hydrogeologist', 'Arts development officer', 'Ceramics designer',
       'Dancer', 'Conservator, furniture',
       'Environmental education officer', 'Early years teacher',
       'Sales promotion account executive', 'Records manager',
       'Media buyer', 'Surveyor, mining', 'Statistician', 'Music tutor',
       'Community pharmacist', 'Neurosurgeon', 'Plant breeder/geneticist',
       'Conservation officer, historic buildings',
       'English as a foreign language teacher', 'Biomedical engineer',
       'Dealer', 'Teaching laboratory technician', "Barrister's clerk",
       'Engineer, technical sales', 'Health and safety adviser',
       'Patent attorney', 'Diagnostic radiographer',
       'Administrator, local government', 'Learning disability nurse',
       'Community education officer', 'Drilling engineer',
       'Clinical biochemist', 'Psychotherapist, child',
       'Professor Emeritus', 'Race relations officer',
       'Volunteer coordinator', 'Mudlogger', 'Herpetologist',
       'Insurance risk surveyor', 'Retail manager', 'Careers adviser',
       'Conservator, museum/gallery', 'Designer, television/film set',
       'Restaurant manager, fast food', 'Associate Professor',
       'Wellsite geologist', 'Engineer, civil (contracting)',
       'Exhibition designer', 'Agricultural consultant',
       'Warehouse manager', 'Clinical research associate',
       'Purchasing manager', 'Information systems manager',
       'Chief Marketing Officer', 'Television floor manager',
       'Textile designer', 'Production assistant, television',
       'Software engineer', 'Market researcher',
       'Garment/textile technologist', 'Radiographer, therapeutic',
       'Sports development officer', 'Aeronautical engineer',
       'Sales professional, IT', 'Equities trader', 'Hospital pharmacist',
       'Air traffic controller', 'Engineer, aeronautical',
       'Database administrator', 'Personnel officer', 'Health visitor',
       'Operational researcher', 'Amenity horticulturist',
       'Industrial/product designer', 'Orthoptist',
       'Clinical psychologist', 'Embryologist, clinical',
       'Advertising account executive', 'Engineer, materials',
       'Child psychotherapist', 'Illustrator', 'Primary school teacher',
       'Lecturer, further education', 'Loss adjuster, chartered',
       'Engineer, water', 'Water quality scientist', 'Psychiatric nurse',
       'Aid worker', 'Travel agency manager',
       'Higher education careers adviser', 'Insurance underwriter',
       'Therapist, music', 'Product designer',
       'Advertising account planner', 'Fisheries officer',
       'Control and instrumentation engineer',
       'Nature conservation officer', 'Social researcher',
       'Public house manager', 'Scientist, research (physical sciences)',
       'Scientist, research (medical)', 'Ambulance person',
       'Airline pilot', 'Broadcast journalist', 'Media planner',
       'Teacher, primary school', 'Air broker', 'Insurance broker',
       'Field seismologist', 'Animator', 'Academic librarian',
       'Public relations officer', 'Psychologist, clinical',
       'Medical technical officer', 'Medical physicist',
       'Charity fundraiser', 'Retail merchandiser', 'Engineer, site',
       'Occupational therapist', 'Counselling psychologist',
       'Metallurgist', 'Electrical engineer', 'Hydrographic surveyor',
       'Tour manager', 'Furniture conservator/restorer',
       'Architectural technologist', 'Copy', 'Waste management officer',
       'Writer', 'Leisure centre manager', 'Maintenance engineer',
       'Civil Service administrator', 'Building services engineer',
       'Production assistant, radio',
       'Museum/gallery exhibitions officer',
       'Social research officer, government', 'Animal technologist',
       'Intelligence analyst', 'Engineer, manufacturing', 'Buyer, retail',
       'Art gallery manager', 'Rural practice surveyor', 'Quarry manager',
       'Pharmacologist', 'Interpreter',
       'Armed forces logistics/support/administrative officer',
       'Contracting civil engineer', 'Environmental health practitioner',
       'Designer, textile', 'Solicitor, Scotland', 'Catering manager',
       'Interior and spatial designer', 'Therapist, drama',
       'Surveyor, hydrographic', 'Accountant, chartered',
       'Broadcast engineer', 'Psychotherapist', 'Nurse, mental health',
       'IT consultant', 'Hotel manager', 'Merchandiser, retail',
       'Veterinary surgeon', 'Manufacturing engineer',
       'Geophysicist/field seismologist', 'Marketing executive',
       'Industrial buyer', 'Information officer',
       'Estate manager/land agent', 'Data scientist',
       'Armed forces technical officer', 'Homeopath',
       'Environmental manager', 'Forest/woodland manager',
       'Dance movement psychotherapist', 'Location manager',
       'Ship broker', 'Ecologist', 'Magazine journalist',
       'Engineer, communications', 'Administrator, arts', 'Stage manager',
       'Teacher, adult education', 'Education officer, community',
       'Local government officer'
]

# Formulaire pour saisir les données utilisateur
st.write('Remplissez le formulaire pour prédire la fraude.')

form = st.form(key='input_form')
amt = form.number_input('Montant de la transaction', min_value=0.0, value=0.0, help='', key='amt')
zip_code = form.text_input('Code postal', placeholder='Entrez le code postal')
city_pop = form.number_input('Population de la ville', min_value=0, help='')
unix_time = form.number_input('Heure de la transaction (Unix time)', value=0, help='')
category = form.selectbox('Catégorie', options=categories, help='')
gender = form.selectbox('Genre', options=genders, help='')
street = form.text_input('Nom de la rue', placeholder='Entrez le nom de la rue')
city = form.text_input('Ville', placeholder='Entrez le nom de la ville')
state = form.text_input('État', placeholder='Entrez le nom de l\'État')
job = form.selectbox('Emploi' ,options=job_options, help='')



# Champ de saisie pour le numéro de transaction
trans_num = form.text_input('Numéro de transaction')

submit_button = form.form_submit_button(label='Prédire')

# Faire la prédiction lorsque l'utilisateur appuie sur le bouton "Prédire"
if submit_button:
    if len(trans_num) != 32:
        st.error("Le numéro de transaction doit avoir une longueur de 32 caractères.")
    else:
        # Charger le modèle enregistré
        loaded_model = joblib.load('fraud_detection_model.pkl')
        # Préparer les données de l'utilisateur pour la prédiction
        user_data = pd.DataFrame({
            'amt': [amt],
            'zip': [zip_code],
            'city_pop': [city_pop],
            'unix_time': [unix_time],
            'category': [category],
            'gender': [gender],
            'street': [street],
            'city': [city],
            'state': [state],
            'job': [job],
            'trans_num': [trans_num]
        })
        # Faire la prédiction
        prediction = loaded_model.predict(user_data)
        # Afficher la prédiction
        if prediction[0] == 1:
            st.write('Fraude détectée!')
        else:
            st.write('Aucune fraude détectée.')
if __name__ == "__main__":
    main()
