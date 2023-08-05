# Hector --- A collection manager.
# Copyright © 2023 Bioneland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

hector = Hector

menu-books = Livres
menu-login = Se connecter
menu-logout = Se déconnecter

# version (string) The version of the software.
# years (string) The years the copyright applies to.
# holders (string) The names of the copyright holders.
copyright = Version { $version } © { $years } { $holders }.

# name (string) The name of the license.
# url (string) The URL of the license file.
license = Le code est sous licence <a href="{ $url }">{ $name }</a>.

# name (string) The name of the information to display
# value (string) The value of the information to display
info-line = { $name } : { $value }

access-forbidden = Accès interdit !
access-unauthorised = Accès non authorisé !
an-error-occurred = Une erreur s'est produite !

book = livre
books = livres
book-isbn = ISBN
book-isbn-description = Le numéro ISBN assigné au livre, par exemple 978-0-7653-9277-0.
book-title = titre
book-title-description = Le titre du livre.
book-year = année
book-year-description = L'année de publication du livre.
book-author = aut·rice·eur
book-author-description = Un·e des aut·rice·eur·s du livre.
book-authors = aut·rice·eur·s
book-authors-description = La liste des aut·rice·eur·s du livre, séparé·e·s par des virgules.
book-genre = genre
book-genre-description = Un des genres auxquels le livre se rattache.
book-genres = genres
book-genres-description = La liste des genres auxquels le livre se rattache, séparés par des virgules.

mandatory-value = Cette valeur est obligatoire !
incorrect-value = Cette valeur est incorrecte !
not-an-isbn = Ceci n'est pas un ISBN !

auth-login-title = Connexion
# method (string) The sign in method
auth-login-method = Sign in using { $method }

webauthn-register-title = Association du dispositif de sécurité
webauthn-register-description = Votre navigateur devrait être en train de vous demander de toucher votre dispositif de sécurité…
webauthn-register-success = Votre dispositif de sécurité a été correctement associé !
webauthn-register-failure = Votre dispositif de sécurité n'a pas pu être associé !?

webauthn-login-title = Connexion
webauthn-login-description = Votre navigateur devrait être en train de vous demander de toucher votre dispositif de sécurité…
webauthn-login-failure = Vous n'avez pas pu être connecté·e !?

add-book-requires-authentification = Vous devez être authentifié·e pour pouvoir ajouter un livre !
add-book-title = Ajouter un nouveau livre à la collection
add-book-action = Ajouter un livre
add-book-cancel = Annuler
add-book-add = Ajouter

search-books-title = Chercher un livre dans la collection
search-books-action = Chercher un livre
search-books-clear = Réinitialiser
search-books-search = Chercher
search-books-no-result = Aucun livre ne correspond !
search-books-previous-page = Précédent
search-books-next-page = Suivant

# title (string) The title of the book
display-book-title = Détails pour « { $title } »

update-book-requires-authentification = Vous devez être authentifié·e pour pouvoir éditer un livre !
# isbn (string) The ISBN of the book
update-book-title = Éditer les informations de `{ $isbn }`
update-book-action = Éditer
update-book-failure = Le livre n'a pas pu être mis à jour !
update-book-success = Le livre a bien été mis à jour !
update-book-cancel = Annuler
update-book-update = Enregistrer

book-already-exists = Ce livre est déjà dans la collection !
book-added = Le livre a bien été ajouté.
book-not-found = Le livre n'a pas été trouvé !
book-cannot-be-added = Le livre n'a pas pu être ajouté !
books-cannot-be-found = La recherche n'a pas pu être effectuée !
