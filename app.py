from flask import Flask, request, render_template, redirect, url_for, flash
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime 

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 

# MongoDB connection
client = MongoClient('mongodb+srv://Vivek27951:Enyb4Za5h9PP962@sandbox.0r8nd.mongodb.net/')
db = client['notes_app']
notes_collection = db['notes']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        if content:
            note = {
                'content': content,
                'timestamp': datetime.now() 
            }
            notes_collection.insert_one(note)
            flash('Note added successfully', 'success')
            return redirect(url_for('index'))

    notes = notes_collection.find()
    return render_template('index.html', notes=notes)

@app.route('/update/<note_id>', methods=['GET', 'POST'])
def update(note_id):
    if request.method == 'POST':
        new_content = request.form['new_content']
        if new_content:
            notes_collection.update_one(
                {'_id': ObjectId(note_id)},
                {'$set': {'content': new_content}}
            )
            flash('Note updated successfully', 'success')
            return redirect(url_for('index'))
    
    note = notes_collection.find_one({'_id': ObjectId(note_id)})
    if note:
        return render_template('update.html', note=note)
    else:
        flash('Note not found', 'danger')
        return redirect(url_for('index'))

@app.route('/delete/<note_id>', methods=['GET'])
def delete(note_id):
    print("note_id -> ",note_id)
    try:
        result = notes_collection.delete_one({'_id': ObjectId(note_id)})
        if result.deleted_count == 1:
            flash('Note deleted successfully', 'success')
        else:
            flash('Note not found', 'danger')
    except Exception as e:
        flash(str(e), 'danger')
    
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']
        notes = notes_collection.find({'content': {'$regex': search_query, '$options': 'i'}})
        return render_template('search.html', notes=notes, search_query=search_query)
    
    return render_template('search.html', notes=[])

if __name__ == '__main__':
    app.run(debug=True)
