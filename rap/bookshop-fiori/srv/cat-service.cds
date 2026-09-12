using { my.bookshop as my } from '../db/schema';

service CatalogService {
    @odata.draft.enabled
    entity Books as projection on my.Books
    actions {
        action Publish() returns Books;
    };
}

annotate CatalogService.Books with @(
    UI.SelectionFields : [
        category,
        status
    ]
);

