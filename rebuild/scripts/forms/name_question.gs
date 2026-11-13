// Adds one optional question, "Your name", as the first question of the six marking forms, so that the people
// who marked can be thanked by name in the acknowledgements. Run addNameQuestion once (13 Nov 2026); running it
// again changes nothing. The answer lands in a new last column of each "Form responses N" tab, so the columns
// that the Results tab counts do not move.

var NAME_FORM_IDS = {
  A: '1D4c0p7wr5No1ShSDpS-Bq8HbHdsKZg8bttndmo0vsTQ',
  B: '1QDNhaClE_dLZ_yVqh5hlCyJfxk2modxC-MGqo4L6sig',
  C: '1PDzvEHKvS31v1YpwrQFVdOPetelHqU5qV3CfM2TtfQE',
  D: '1DETnembQ8NYya_8FS4HoOFWZBoMMhKtn5D5O9NszSVQ',
  E: '1hnY7O9M4RM9j_rF2Pbo9ZDFz0tWwPS0HK9YuwL9XP0A',
  F: '1m_MMdZQ8alxvmam4UYT7C3gtsz0rnkbV0x36VvtZh8U'
};
var NAME_TITLE = 'Your name and institution (optional)';
var NAME_HELP =
  'We would like to thank the people who marked these statements, by name, in the acknowledgements of the paper ' +
  'about this evaluation. Write your name as you want it printed. Leave this empty to stay anonymous: your marks ' +
  'count either way.';

function addNameQuestion() {
  var out = Object.keys(NAME_FORM_IDS).map(function (k) {
    var f = FormApp.openById(NAME_FORM_IDS[k]);
    var items = f.getItems();
    var has = items.some(function (it) { return it.getTitle() === NAME_TITLE; });
    if (!has) {
      var it = f.addTextItem().setTitle(NAME_TITLE).setHelpText(NAME_HELP).setRequired(false);
      f.moveItem(it.getIndex(), 0);
    }
    var after = f.getItems();
    return k + ': ' + (has ? 'already there' : 'added') + ', items ' + items.length + ' -> ' + after.length +
      ', first = "' + after[0].getTitle() + '", responses ' + f.getResponses().length;
  });
  Logger.log('NAMEQ ' + out.join(' | '));
  return out;
}
