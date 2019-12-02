# Analyse der Bahnpreise während der Rabattaktion vom Herbst 2019

**Wie teuer ist Zugfahren in Zeiten der Sparbillettschwemme? Eine Analyse der aus dem Fahrplan ausgelesenen Preise für ausgewählte Strecken.**

###Projektbeschrieb

Im Herbst 2019 wurden auf der [Website der SBB](https://www.sbb.ch) auffallend viele vergünstigte Billettte feilgeboten. Um herauszufinden, ob dieser subjektive Eindruck trügt, haben wir das Angebot während zweieinhalb Monaten systematisch untersucht. Vom 11. September bis zum 24. November haben wir mit einem von einem Computerskript gesteuerten Webbrowser (Scraper in Python mit Selenium) täglich die SBB-Website aufgerufen. Abgefragt wurden die Preise für Fahrten in 1, 3, 7, 14, 30 und 60 Tagen für ausgewählte Strecken zwischen grossen Städten im Tamedia-Stammgebiet sowie für beliebte Wochenenddestinationen. Die Resultate wurden abgespeichert. In einem zweiten Schritt wurden die Verbindungs- und Preisinformationen mit einem weiteren Skript (Python mit BeautifulSoup) ausgelesen. Entstanden ist ein Datensatz mit gut 180’000 Preisen für 120’000 Fahrten zwischen dem 12. September und dem 20. Januar 2020. Die Detailinformationen zur weiteren Aufbereitung und Auswertung der Daten sind in den beiden untenstehenden Jupyter Notebooks zu finden. Aus den Daten ist ein Artikel für die Sonntagszeitung entstanden, der [auch online publiziert](https://www.tagesanzeiger.ch/wirtschaft/die-sbb-ueberschwemmen-den-markt-mit-sparbilletten/story/11571463) wurde. 

In diesem Repo sind zwei Jupyter Notebooks zu finden: 

**2_sparbillette_aufbereitung** wird benötigt, um die vom Scraper gesicherten und anschliessend ausgelesenen Rohdaten aufzubereiten. 

**3_sparbillette_auswertung** ist die eigentliche Datenauswertung. 

In diesem Repo nicht enthalten ist der Scraper sowie das Skript zum Auslesen der Daten aus den HTML-Dateien. Beide sind auf Nachfrage verfügbar. 

Autor: [Mathias Born](mailto:mathias.born@tamedia.ch)
