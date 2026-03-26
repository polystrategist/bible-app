<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class UserNote extends Model
{
    use HasFactory;

    protected $table = 'user_notes';

    protected $fillable = [
        'user_id',
        'study_space_name',
        'content',
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
