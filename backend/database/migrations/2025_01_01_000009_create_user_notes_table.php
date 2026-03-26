<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('user_notes', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->string('study_space_name')->default('default');
            $table->longText('content')->nullable();
            $table->timestamps();

            $table->unique(['user_id', 'study_space_name']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('user_notes');
    }
};
