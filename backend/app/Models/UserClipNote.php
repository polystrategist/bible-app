<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class UserClipNote extends Model
{
    use HasFactory;

    protected $table = 'user_clip_notes';

    protected $fillable = [
        'user_id',
        'study_space_name',
        'key',
        'book_number',
        'chapter',
        'verse',
        'content',
        'color',
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
