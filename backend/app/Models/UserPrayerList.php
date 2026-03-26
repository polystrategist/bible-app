<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class UserPrayerList extends Model
{
    use HasFactory;

    protected $table = 'user_prayer_lists';

    protected $fillable = [
        'user_id',
        'key',
        'title',
        'content',
        'group',
        'index',
        'status',
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
