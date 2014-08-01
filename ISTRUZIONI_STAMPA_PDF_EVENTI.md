
ISTRUZIONI PER STAMPARE I PDF 
=============================

PDF con informazioni eventi
---------------------------

- cd /var/www/event_manager
- rm info-pdf/*.pdf
- ./manage.py print_events_info
- pdftk info_pdf/*-1.pdf cat output /tmp/info_eventi_turno1.pdf
- pdftk info_pdf/*-2.pdf cat output /tmp/info_eventi_turno2.pdf
- pdftk info_pdf/*-3.pdf cat output /tmp/info_eventi_turno3.pdf

PDF con iscritti eventi
---------------------------

- cd /var/www/event_manager
- rm iscritti-pdf/*.pdf
- ./manage.py print_events_iscritti
- pdftk iscritti_pdf/*-1.pdf cat output /tmp/iscritti_eventi_turno1.pdf
- pdftk iscritti_pdf/*-2.pdf cat output /tmp/iscritti_eventi_turno2.pdf
- pdftk iscritti_pdf/*-3.pdf cat output /tmp/iscritti_eventi_turno3.pdf

