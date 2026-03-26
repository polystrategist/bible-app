<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('user_prayer_lists', function (Blueprint $table) {
            // Drop the global unique index on key alone (allows key collision across users)
            $table->dropUnique(['key']);
            // Replace with a per-user unique constraint
            $table->unique(['user_id', 'key']);
        });
    }

    public function down(): void
    {
        Schema::table('user_prayer_lists', function (Blueprint $table) {
            $table->dropUnique(['user_id', 'key']);
            $table->unique(['key']);
        });
    }
};
