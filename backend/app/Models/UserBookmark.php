<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class UserBookmark extends Model
{
    use HasFactory;

    protected $table = 'user_bookmarks';

    protected $fillable = [
        'user_id',
        'study_space_name',
        'key',
        'book_number',
        'chapter',
        'verse',
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
