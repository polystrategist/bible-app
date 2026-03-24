<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class SyncLog extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'table_name',
        'record_key',
        'action',
        'payload',
        'synced',
    ];

    protected $casts = [
        'payload' => 'array',
        'synced' => 'boolean',
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
